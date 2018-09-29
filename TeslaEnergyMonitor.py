import PersistTimeSeries as PersistTimeSeries
import time 


p = PersistTimeSeries.PersistTimeSeries()
while True: 
    p.persistBatteryLevel()
    time.sleep(30)