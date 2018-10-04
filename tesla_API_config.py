import os, glob
import json
from os.path import isfile, join
import io
import time
import sys
import logging
import datetime

logging.basicConfig(filename='./logs/tesla_API_config.log', level=logging.INFO)


class TeslaAPIConfig(): 
    __vehicles = []  # contains all the log data that is aviable on disk

    def __init__(self):
        # first read in all the logFiles
        self.__vehicles = self.load_vehicles()

    # This function read the logfiles in the folder /Logs and return 
    # a dictionary with the JSON data
    def load_vehicles(self):
        data = []
        try:
            with io.open("tesla_API.config", 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            logging.error(str(datetime.datetime.now()) + '==> Load ==> Opening config file failed :  ' + str(e))
            print("The config file could (tesla_API.config) not be read. Is it in the main folder?")
        finally:
            f.close()