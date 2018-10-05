from telegraf.client import TelegrafClient
import tesla_API_vehicle
import tesla_API_config
import datetime
import pprint
import logging 
import json
import datetime 


class PersistTimeSeries(): 
    logging.basicConfig(filename='./logs/persist_time_series.log', level=logging.INFO)
    __vehicles = []
    __telegrafClient = '' 

    def __init__(self): 
        # Read the config file with all the vehicle settings in it
        config = tesla_API_config.TeslaAPIConfig()
        vehiclesConfig = config.load_vehicles() 
        logging.info(str(datetime.datetime.now()) + '==> PersistTimeSeries ==> Config file is loaded ')

        # Create an dict of instances of TelsaAPIVehicles
        amountOfVehicles = len(vehiclesConfig["Vehicles"])
        counterVehiclesRead = 0
        while (counterVehiclesRead < amountOfVehicles): 
            vehicle = tesla_API_vehicle.Vehicle(vehiclesConfig["Vehicles"][counterVehiclesRead]['email'], vehiclesConfig["Vehicles"][counterVehiclesRead]['password'])
            self.__vehicles.append(vehicle)
            counterVehiclesRead = counterVehiclesRead + 1

        # Create the TelegrafClient 
        self.__telegrafClient = TelegrafClient(host='localhost', port=8092)

    def persist_vehicles_state(self): 
        for vehicle in self.__vehicles:
            try:
                charge_state = vehicle.get_charge_state()
                self.__telegrafClient.metric('battery_level', charge_state['battery_level'], 
                                             tags={'vehicleID': str(vehicle.get_vehicleID()),
                                             'vehicle_name': vehicle.get_vehicle_name()})
                self.__telegrafClient.metric('battery_range', charge_state['battery_range'], 
                                             tags={'vehicleID': str(vehicle.get_vehicleID()),
                                             'vehicle_name': vehicle.get_vehicle_name()})

                climate_state = vehicle.get_climate_state()
                self.__telegrafClient.metric('outside_temp', climate_state['outside_temp'], 
                                             tags={'vehicleID': str(vehicle.get_vehicleID()),
                                             'vehicle_name': vehicle.get_vehicle_name()})
                self.__telegrafClient.metric('inside_temp', climate_state['inside_temp'], 
                                             tags={'vehicleID': str(vehicle.get_vehicleID()),
                                             'vehicle_name': vehicle.get_vehicle_name()})

                vehicle_state = vehicle.get_vehicle_state()
                self.__telegrafClient.metric('odometer', vehicle_state['odometer'], 
                                             tags={'vehicleID': str(vehicle.get_vehicleID()),
                                             'vehicle_name': vehicle.get_vehicle_name()})
            except Exception as e: 
                logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.persist_charge_state ==> failed ' + str(e))
