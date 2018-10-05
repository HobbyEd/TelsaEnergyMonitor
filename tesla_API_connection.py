import requests
import json
import logging
import datetime
import pprint
import calendar


class Connection():
    logging.basicConfig(filename='./logs/tesla_API_connection.log', level=logging.INFO)
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

