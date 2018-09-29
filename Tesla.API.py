import requests
import json 
import logging 
import datetime
import pprint

logging.basicConfig(filename='./logs/Tesla.API.Connection.log', level=logging.INFO)



class Connection():
    authenticationURL =  "https://owner-api.teslamotors.com/oauth/token"
    access_token = '' 
    email = ''
    password = ''
    grantType = 'password'
    clientID = '' 
    clientSecret = ''

    def __init__(self,
            email='',
            password=''):
        self.email = email
        self.password = password

    # Authentication of the user by Tesla 
    # Returns: access_token, which must be provided by each call to the Tesla API
    def getAccessToken(self): 
        # when first time authentication get the clientID and ClientSecret
        if (not self.clientID):
            self.getClientIDandSecret()

        data = {'email': self.email, 
                'password': self.password, 
                'grant_type': self.grantType, 
                'client_id': self.clientID, 
                'client_secret': self.clientSecret}
        try:
            r = requests.post(self.authenticationURL, json=data)
            if (r.status_code == 200):
                data = r.json()
                self.access_token = data["access_token"]
                return self.access_token
            else:
                logging.error(str(datetime.datetime.now()) + '==> Connection.getAccessToken ==> Rest call returned wrong status code: ', + str(r.status_code))
        except Exception as e:
            logging.error(str(datetime.datetime.now()) + '==> Connection.getAccessToken ==> Rest call failed ' + str(e))

    def getClientIDandSecret(self):
        try: 
            r = requests.get("http://pastebin.com/raw/0a8e0xTJ")
            if (r.status_code == 200): 
                data = r.json()
                self.clientID = data['v1']['id']
                self.clientSecret = data['v1']['secret']
            else:
                logging.warn(str(datetime.datetime.now()) + '==> Connection.getClientIDandSecret ==> Rest call returned wrong status code: ', + str(r.status_code))
        except Exception as e:
            logging.error(str(datetime.datetime.now()) + '==> Connection.getClientIDandSecret ==> Rest call failed ' + str(e))
        return r

class Vehicle():
    vehicleListURL = "https://owner-api.teslamotors.com/api/1/vehicles"
    chargeStateURL = "https://owner-api.teslamotors.com/api/1/vehicles/vehicle_id/data_request/charge_state"
    vehicleID = '' 

    def __init__(self, email, password):
        con = Connection(email, password)
        self.connection = con
        self.setVehicleID()

    #The API assumes there is only one Tesla on the account provided 
    def setVehicleID(self): 
        head = {"Authorization": "Bearer %s" % self.connection.getAccessToken()}
        if (not self.vehicleID): 
            try:
                r = requests.get(self.vehicleListURL, headers=head )
                data = r.json()
                self.vehicleID = data['response'][0]['id']
                logging.info(str(datetime.datetime.now()) + '==> Vehicle.setVehicleID ==> Returned vehicleID: ' + str(self.vehicleID))
            except Exception as e:
                logging.error(str(datetime.datetime.now()) + '==> Connection.getVehicle ==> Rest call failed' + str(e))
        
    def getBatteryState(self): 
        self.chargeStateURL = self.chargeStateURL.replace('vehicle_id', str(self.vehicleID))
        batteryState = {}
        head = {"Authorization": "Bearer %s" % self.connection.getAccessToken()}
        try:
            r = requests.get(self.chargeStateURL, headers=head)
            data = r.json()
            batteryState['batteryLevel'] = data['response']['battery_level']
            batteryState['batteryRange'] = data['response']['battery_range']
            batteryState['timeStamp']  = data['response']['timestamp']
        except Exception as e: 
            logging.error(str(datetime.datetime.now()) + '==> Connection.getChargeState ==> Rest call failed' + str(e))



