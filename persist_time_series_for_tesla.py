from telegraf.client import TelegrafClient
from geolib import geohash
import tesla_API_vehicle
import tesla_API_config
import datetime
import pprint
import logging 
import json
import datetime 


class PersistTimeSeriesForTesla(): 
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

    def __persist_charge_state(self, vehicle):
        # get the charge_state: this contains battery information
        try:
            charge_state = vehicle.get_charge_state()
            self.__telegrafClient.metric('battery_level', charge_state['battery_level'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
            self.__telegrafClient.metric('battery_range', charge_state['ideal_battery_range'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
            if (charge_state['charging_state'].upper() == 'Charging'.upper()):
                location = geohash.encode(charge_state['latitude'], charge_state['longitude'], 7)
                logging.info(str(datetime.datetime.now()) + '==> Charging on location: ' + location + ' with value : ' + str(charge_state['charge_energy_added']) )
                self.__telegrafClient.metric('charge_energy_added', charge_state['charge_energy_added'], 
                                            tags={'vehicleID': str(vehicle.get_vehicleID()),
                                            'vehicle_name': vehicle.get_vehicle_name(), 
                                            'location': location})
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.__persist_charge_state ==> failed ' + str(e))

    def __persist_climate_state(self, vehicle):
        # climate data contains the temperature of the car and outside
        try:
            climate_state = vehicle.get_climate_state()
            self.__telegrafClient.metric('outside_temp', climate_state['outside_temp'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
            self.__telegrafClient.metric('inside_temp', climate_state['inside_temp'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.__persist_climate_state ==> failed ' + str(e))     

    def __persist_vehicle_state(self, vehicle):
        try:
            # Vehicle data contains the odometer
            vehicle_state = vehicle.get_vehicle_state()
            self.__telegrafClient.metric('odometer', vehicle_state['odometer'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.__persist_vehicle_state ==> failed ' + str(e))       

    def __persist_drive_state(self, vehicle):
        try:
            # Vehicle data contains the odometer
            vehicle_state = vehicle.get_drive_state()
            self.__telegrafClient.metric('power', vehicle_state['power'], 
                                         tags={'vehicleID': str(vehicle.get_vehicleID()),
                                         'vehicle_name': vehicle.get_vehicle_name()})
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.__persist_drive_state ==> failed ' + str(e))   

    def persist_vehicles_state(self): 
        for vehicle in self.__vehicles:
            try:
                # first make sure the vehicle gets the latest data from Tesla.
                vehicle.get_vehicle_data_from_tesla()
                # persist all the subsets of data
                self.__persist_charge_state(vehicle)
                self.__persist_climate_state(vehicle)
                self.__persist_vehicle_state(vehicle)
                self.__persist_drive_state(vehicle)
            except Exception as e: 
                logging.error(str(datetime.datetime.now()) + '==> PersistTimeSeries.persist_vehicle_state ==> failed ' + str(e))
