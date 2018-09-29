from telegraf.client import TelegrafClient
import TeslaAPI
import TeslaAPIConfig
import datetime
import pprint
import logging 
import json
import datetime 

logging.basicConfig(filename='./logs/PersistTimeSeries.log', level=logging.INFO)

class PersistTimeSeries(): 
    vehicles = []
    telegrafClient = '' 

    def __init__(self): 
        # Read the config file with all the vehicle settings in it
        Config = TeslaAPIConfig.TeslaAPIConfig()
        vehiclesConfig = Config.loadVehicles() 
        logging.info(str(datetime.datetime.now()) + '==> PersistTimeSeries ==> Config file is loaded ')

        #Create an dict of instances of TelsaAPIVehicles
        amountOfVehicles = len(vehiclesConfig["Vehicles"])
        counterVehiclesRead = 0
        while (counterVehiclesRead < amountOfVehicles): 
            vehicle = TeslaAPI.Vehicle(vehiclesConfig["Vehicles"][counterVehiclesRead]['email'], vehiclesConfig["Vehicles"][counterVehiclesRead]['password'])
            self.vehicles.append(vehicle)
            counterVehiclesRead = counterVehiclesRead + 1

        #Create the TelegrafClient 
        self.telegrafClient = TelegrafClient(host='localhost', port=8092)

    def persistBatteryLevel(self): 
        for object in self.vehicles:
            try:
                battery = object.getBatteryState()
                self.telegrafClient.metric('batteryLevel', battery['batteryLevel'], tags={'vehicleID': battery['vehicleID']})
            except Exception as e: 
                logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.persistBatteryLevel ==> failed ' + str(e))


