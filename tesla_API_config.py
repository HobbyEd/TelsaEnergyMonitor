import os, glob
import json
from os.path import isfile, join
import io
import time
import sys
import logging
import datetime


class TeslaAPIConfig(): 
    logging.basicConfig(filename='./logs/tesla_API_config.log', level=logging.INFO)
    __vehicles = []  # contains all the log data that is aviable on disk

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