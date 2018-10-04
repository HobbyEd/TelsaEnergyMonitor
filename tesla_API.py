import requests
import json
import logging
import datetime
import pprint
import calendar

logging.basicConfig(filename='./logs/TeslaAPIConnection.log', level=logging.INFO)


class Connection():
    __authentication_URL = "https://owner-api.teslamotors.com/oauth/token"
    __access_token = ''
    __email = ''
    __password = ''
    __grant_type = 'password'
    __clientID = ''
    __client_secret = ''
    __expiration = ''

    def __init__(self,
                email='',
                password=''):
        self.__email = email
        self.__password = password 

    # Authentication of the user by Tesla 
    # Returns: access_token, which must be provided by each call to the Tesla API
    def get_access_token(self): 
        # when first time authentication get the clientID and ClientSecret
        if (not self.__clientID):
            self.get_clientID_and_secret()
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if (not self.__expiration) or (now > self.__expiration):  
            try:
                data = {'email': self.__email, 
                        'password': self.__password, 
                        'grant_type': self.__grant_type, 
                        'client_id': self.__clientID, 
                        'client_secret': self.__client_secret}
                r = requests.post(self.__authentication_URL, json=data)
                if (r.status_code == 200):
                    data = r.json()
                    self.__access_token = data["access_token"]
                    self.__expiration = data['created_at'] + data['expires_in'] - 86400
                    return self.__access_token
                else:
                    logging.error(str(datetime.datetime.now()) + '==> Connection.get_access_token ==> Rest call returned wrong status code: ', + str(r.status_code))
            except Exception as e:
                logging.error(str(datetime.datetime.now()) + '==> Connection.get_access_token ==> Rest call failed ' + str(e))
        else: 
            return self.__access_token

    def get_clientID_and_secret(self):
        try: 
            r = requests.get("http://pastebin.com/raw/0a8e0xTJ")
            if (r.status_code == 200): 
                data = r.json()
                self.__clientID = data['v1']['id']
                self.__client_secret = data['v1']['secret']
            else:
                logging.warn(str(datetime.datetime.now()) + '==> Connection.get_clientID_and_secret ==> Rest call returned wrong status code: ', + str(r.status_code))
        except Exception as e:
            logging.error(str(datetime.datetime.now()) + '==> Connection.get_clientID_and_secret ==> Rest call failed ' + str(e))


class Vehicle():
    __vehicle_list_URL = "https://owner-api.teslamotors.com/api/1/vehicles"
    __charge_state_URL = "https://owner-api.teslamotors.com/api/1/vehicles/vehicle_id/data_request/charge_state"
    __vehicle_ID = '' 

    def __init__(self, email, password):
        _con = Connection(email, password)
        self.__connection = _con
        self.set_vehicleID()

    # The API assumes there is only one Tesla on the account provided 
    def set_vehicleID(self): 
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
                logging.error(str(datetime.datetime.now()) + '==> Connection.get_vehicle ==> Rest call failed' + str(e))
        
    def get_battery_state(self): 
        self.__charge_state_URL = self.__charge_state_URL.replace('vehicle_id', str(self.__vehicle_ID))
        battery_state = {}
        head = {"Authorization": "Bearer %s" % self.__connection.get_access_token()}
        try:
            r = requests.get(self.__charge_state_URL, headers=head)
            data = r.json()
            battery_state['vehicleID'] = str(self.__vehicle_ID)
            battery_state['batteryLevel'] = data['response']['battery_level']
            battery_state['batteryRange'] = data['response']['battery_range']
            battery_state['timeStamp'] = data['response']['timestamp']
            return battery_state
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> Connection.get_battery_state ==> Rest call failed : ' + str(e))