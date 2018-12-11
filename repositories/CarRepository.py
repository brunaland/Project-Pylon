import csv
from models.Car import Car
from datetime import datetime, timedelta
import operator


class CarRepository:
    
    def __init__(self):
        self.__carsUnavailable = []
        self.__carsAvailable = []
        self.__carLicenseplates = set()
        self.__carsCUVAvailable= []
        self.__carsLuxuryAvailable = []
        self.__carsHighlandAvailable = []
        self.__carsCompactAvailable = []
        self.__carsComfortAvailable = []
        self.__carsCUVUnavailable= []
        self.__carsLuxuryUnavailable = []
        self.__carsHighlandUnavailable = []
        self.__carsCompactUnavailable = []
        self.__carsComfortUnavailable = []

    def addCar(self, newCar):
        with open('./data/cars.csv', 'a') as carFile:
            carType = newCar.getType()
            make = newCar.getMake()
            color = newCar.getColor()
            passengers = newCar.getPassengers()
            transmission = newCar.getTransmission()
            licenseplate = newCar.getLicenseplate()
            rentCost = newCar.getRentcost()
            status = newCar.getStatus()
            rentOutCar = newCar.getRentOutCar()
            returnCar = newCar.getReturnCar()
            
            carFile.write("{},{},{},{},{},{},{},{},{},{}\n".format(carType,make,licenseplate,color,passengers,transmission,\
            rentCost,status,rentOutCar,returnCar))

    def createDate(self, rentDate):
        day, month, year, hour, minutes = map(int, rentDate.split('-'))
        return datetime(year, month, day, hour, minutes)
       
    def getCars(self, action, typeAction, dateAvailable):
        
        with open('./data/cars.csv', 'r') as carFile:
            csvReader = csv.DictReader(carFile, delimiter=',')

            for line in csvReader:
                carType = line['type']
                make = line['make']
                color = line['color']
                passengers = line['passengers']
                transmission = line['transmission']
                licenseplate = line['licenseplate']
                rentcost = line['rentcost']
                status = line['status']
                rentOutCar = self.createDate(line['rentout'])
                returnCar = self.createDate(line['return'])
                   

                if licenseplate not in self.__carLicenseplates:
                    self.__carLicenseplates.add(licenseplate)
                    newCar = Car(carType, make,licenseplate, color, passengers,transmission, rentcost, status,rentOutCar,returnCar)

                    if rentOutCar < dateAvailable < returnCar or status == 'unavailable':
                        self.__carsUnavailable.append(newCar)  
                        if carType == 'Compact':
                            self.__carsCompactUnavailable.append(newCar)
                        elif carType == 'Comfort':
                            self.__carsComfortUnavailable.append(newCar)  
                        elif carType == 'Luxury':
                            self.__carsLuxuryUnavailable.append(newCar)
                        elif carType == 'CUV':
                            self.__carsCUVUnavailable.append(newCar)  
                        elif carType == 'Highland':
                            self.__carsHighlandUnavailable.append(newCar) 
                    else:
                        self.__carsAvailable.append(newCar)  
                        if carType == 'Compact':
                            self.__carsCompactAvailable.append(newCar)
                        elif carType == 'Comfort':
                            self.__carsComfortAvailable.append(newCar)  
                        elif carType == 'Luxury':
                            self.__carsLuxuryAvailable.append(newCar)
                        elif carType == 'CUV':
                            self.__carsCUVAvailable.append(newCar)  
                        elif carType == 'Highland':
                            self.__carsHighlandAvailable.append(newCar)               
                       
            if action == '1' and typeAction == '':
                return self.__carsAvailable
            elif action == '1' and typeAction == 'compact':
                return self.__carsCompactAvailable
            elif action == '1' and typeAction == 'comfort':
                return self.__carsComfortAvailable
            elif action == '1' and typeAction == 'luxury':
                return self.__carsLuxuryAvailable
            elif action == '1' and typeAction == 'highland':
                return self.__carsHighlandAvailable
            elif action == '1' and typeAction == 'CUV':
                return self.__carsCUVAvailable
            elif action == '2' and typeAction == '':
                return self.__carsUnavailable
            elif action == '2' and typeAction == 'compact':
                return self.__carsCompactUnavailable
            elif action == '2' and typeAction == 'comfort':
                return self.__carsComfortUnavailable
            elif action == '2' and typeAction == 'luxury':
                return self.__carsLuxuryUnavailable
            elif action == '2' and typeAction == 'highland':
                return self.__carsHighlandUnavailable
            elif action == '2' and typeAction == 'CUV':
                return self.__carsCUVUnavailable

    def duplicateLicensePlateCheck(self, newLicensePlate):
        with open('./data/cars.csv', 'r') as customerFile:
            csvReader = csv.DictReader(customerFile)
            for line in csvReader:
                    licensePlate = line['licenseplate']
                    if newLicensePlate == licensePlate:
                        return False
            return True

    def findCar(self, licenseplate, timeOfReturn):
        with open ('./data/cars.csv') as carFile:
            header = ('type','make','licenseplate','color','passengers','transmission','rentcost','status','rentout','return')
            csvReader = csv.DictReader(carFile, header)
            next(carFile, None)
            lines = []
            for line in csvReader:
                if line['licenseplate'] == licenseplate:
                    # Return car befor changes
                    carType = line['type']
                    make = line['make']
                    color = line['color']
                    passengers = line['passengers']
                    transmission = line['transmission']
                    rentcost = line['rentcost']
                    status = line['status']
                    rentOutCar = self.createDate(line['rentout'])
                    returnCar = self.createDate(line['return'])
                    returnCarInfo = Car(carType, make,licenseplate, color, passengers,transmission, rentcost, status,rentOutCar,returnCar)
                    # Change car status
                    line['status'] = 'available'
                    line['return'] = timeOfReturn #strengur
                    lines.append(line)
                else:
                    lines.append(line)
        with open('./data/cars.csv', 'w') as carFile:
            writer = csv.DictWriter(carFile, fieldnames=header)
            writer.writeheader()
            writer.writerows(lines)
            
        return returnCarInfo

    def LicensePlateCheck(self, newLicensePlate):
        with open('./data/cars.csv', 'r') as customerFile:
            csvReader = csv.DictReader(customerFile)
            for line in csvReader:
                    licensePlate = line['licenseplate']
                    if newLicensePlate == licensePlate:
                        carType = line['type']
                        make = line['make']
                        color = line['color']
                        passengers = line['passengers']
                        transmission = line['transmission']
                        rentcost = line['rentcost']
                        status = line['status']
                        rentOutCar = self.createDate(line['rentout'])
                        returnCar = self.createDate(line['return'])
                        returnCarInfo = Car(carType, make,licensePlate, color, passengers,transmission, rentcost, status,rentOutCar,returnCar)
                        return returnCarInfo
            return True

    def editCar(self, carType, make,licenseplate, color, passengers,transmission, rentcost, status,rentOutCar,returnCar):
        with open ('./data/cars.csv') as carFile:
            header = ('type','make','licenseplate','color','passengers','transmission','rentcost','status','rentout','return')
            csvReader = csv.DictReader(carFile, header)
            next(carFile, None)
            lines = []
            for line in csvReader:
                if line['licenseplate'] == licenseplate:
                    # Edit car info.
                    line['status'] = status
                    line['type'] = carType
                    line['make'] = make
                    line['color'] = color
                    line['passengers'] = passengers
                    line['transmission'] = transmission 
                    line['rentcost'] = rentcost
                    line['rentout'] = rentOutCar
                    line['return'] = returnCar
                    lines.append(line)
                    returnCarInfo = Car(carType, make,licenseplate, color, passengers,transmission, rentcost, status,rentOutCar,returnCar)

                else:
                    lines.append(line)
        with open('./data/cars.csv', 'w') as carFile:
            writer = csv.DictWriter(carFile, fieldnames=header)
            writer.writeheader()
            writer.writerows(lines)

        return returnCarInfo