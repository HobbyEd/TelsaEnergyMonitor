import os, glob
import json
from os.path import isfile, join
import io
import time
import sys
import logging 
import datetime

logging.basicConfig(filename='./logs/TeslaAPIConfig.log', level=logging.INFO)

class TeslaAPIConfig(): 
    vehicles = [] #contains all the log data that is aviable on disk
   
    def __init__(self):
        #first read in all the logFiles
        self.vehicles = self.loadVehicles()

    # This function read the logfiles in the folder /Logs and return a dictionary with the JSON data
    def loadVehicles(self):
        data = []
        try:
            with io.open("TeslaAPI.config", 'r', encoding='utf-8') as f:
                data = json.load(f)
                f.close()
            return data
        except Exception as e:
            logging.error(str(datetime.datetime.now()) + '==> Load ==> Opening config file failed :  ' + str(e))
            print("The config file could (TeslaAPI.config) not be read. Is it in the main folder?")