from telegraf.client import TelegrafClient
import tesla_API
import tesla_API_config
import datetime
import pprint
import logging 
import json
import datetime 

logging.basicConfig(filename='./logs/persist_time_series.log', level=logging.INFO)


class PersistTimeSeries(): 
    vehicles = []
    telegrafClient = '' 

    def __init__(self): 
        # Read the config file with all the vehicle settings in it
        config = tesla_API_config.TeslaAPIConfig()
        vehiclesConfig = config.load_vehicles() 
        logging.info(str(datetime.datetime.now()) + '==> PersistTimeSeries ==> Config file is loaded ')

        # Create an dict of instances of TelsaAPIVehicles
        amountOfVehicles = len(vehiclesConfig["Vehicles"])
        counterVehiclesRead = 0
        while (counterVehiclesRead < amountOfVehicles): 
            vehicle = tesla_API.Vehicle(vehiclesConfig["Vehicles"][counterVehiclesRead]['email'], vehiclesConfig["Vehicles"][counterVehiclesRead]['password'])
            self.vehicles.append(vehicle)
            counterVehiclesRead = counterVehiclesRead + 1

        # Create the TelegrafClient 
        self.telegrafClient = TelegrafClient(host='localhost', port=8092)

    def persist_battery_level(self): 
        for object in self.vehicles:
            try:
                battery = object.get_battery_state()
                # print('batteryLevel' + str(battery['batteryLevel']) + 'vehicleID' + str(battery['vehicleID']))
                self.telegrafClient.metric('batteryLevel', battery['batteryLevel'], tags={'vehicleID': battery['vehicleID']})
            except Exception as e: 
                logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.persist_battery_level ==> failed ' + str(e))


