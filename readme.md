# Energy Monitor for devices in house. 
This energy monitor can read data from a Tesla car and the PlugWise Smile P1 device. 

# Dependencies 
This module uses: 

GeoHash

	pip install geolib

Request

	pip install request

XmlToDict

	pip install xmltodict

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

Start the EnergyMonitor

	python EnergyMonitor.py 
