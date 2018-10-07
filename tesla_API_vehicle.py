import requests
import json
import logging
import datetime
import pprint
import tesla_API_connection


class Vehicle():
    logging.basicConfig(filename='./logs/Vehicle.log', level=logging.INFO)
    __vehicle_list_URL = "https://owner-api.teslamotors.com/api/1/vehicles"
    __vehicle_data_URL = "https://owner-api.teslamotors.com/api/1/vehicles/vehicle_id/data"
    __vehicle_ID = '' 
    __vehicle_data = {}
    __miles_to_km = 1.609344
    
    def __init__(self, email, password):
        _con = tesla_API_connection.Connection(email, password)
        self.__connection = _con
        self.__set_vehicleID()

    # The API assumes there is only one Tesla on the account provided 
    def __set_vehicleID(self): 
        head = {"Authorization": "Bearer %s" % self.__connection.get_access_token()}
        if (not self.__vehicle_ID): 
            try:
                r = requests.get(self.__vehicle_list_URL, headers=head)
                data = r.json()
                self.__vehicle_ID = data['response'][0]['id']
                logging.info(str(datetime.datetime.now()) + 
                            '==> Vehicle.setVehicleID ==> Returned vehicleID: ' + 
                            str(self.__vehicle_ID))
            except Exception as e:
                logging.error(str(datetime.datetime.now()) + '==> Vehicle.set_vehicle ==> Rest call failed' + str(e))

    def get_vehicle_data_from_tesla(self):
        self.__vehicle_data_URL = self.__vehicle_data_URL.replace('vehicle_id', str(self.__vehicle_ID))
        head = {"Authorization": "Bearer %s" % self.__connection.get_access_token()}
        try:
            r = requests.get(self.__vehicle_data_URL, headers=head)
            data = r.json()
            self.__vehicle_data = data['response']
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> Connection.get_vehicle_data ==> Rest call failed : ' + str(e))

    def get_vehicleID(self):
        if (self.__vehicle_ID):
            return self.__vehicle_ID
        else: 
            logging.error(str(datetime.datetime.now()) + '==> Vehicle.get_vehicle ==> ' + str(e))

    def get_charge_state(self):
        if (not self.__vehicle_data):
            self.get_vehicle_data_from_tesla()
        self.__vehicle_data['charge_state']['ideal_battery_range'] = self.__vehicle_data['charge_state']['ideal_battery_range'] * self.__miles_to_km
        return self.__vehicle_data['charge_state']

    def get_climate_state(self):
        if (not self.__vehicle_data):
            self.get_vehicle_data_from_tesla()
        return self.__vehicle_data['climate_state']

    def get_vehicle_state(self):
        if (not self.__vehicle_data):
            self.get_vehicle_data_from_tesla()
        self.__vehicle_data['vehicle_state']['odometer'] = self.__vehicle_data['vehicle_state']['odometer'] * self.__miles_to_km
        return self.__vehicle_data['vehicle_state']

    def get_vehicle_name(self):
        if (not self.__vehicle_data):
            self.get_vehicle_data_from_tesla()
        return self.__vehicle_data['display_name']
    
    def get_drive_state(self):
        if (not self.__vehicle_data):
            self.get_vehicle_data_from_tesla()
        return self.__vehicle_data['drive_state']