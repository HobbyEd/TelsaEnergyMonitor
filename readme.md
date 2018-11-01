# Energy Monitor for Tesla cars

# Dependencies 
This module uses: 

GeoHash

	pip install geolib

Request

	pip install request

InfluxDB

	pip install influxdb
	pip install --upgrade influxdb

	
pyTelegraf

	pip install pytelegraf

Download influxDB and Telegraf

Configure Telegraf 

Copy the TeslaAPIExample.config to TeslaAPI.config

Enter the Tesla Account information in the TelsaAPI.config for each car you want to monitor

Start influxd deamon 

Start Telegraf

Start the TeslaEnergyMonitor

	python TeslaEnergyMonitor.py 
