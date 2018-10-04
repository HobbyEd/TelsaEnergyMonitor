import persist_time_series as PersistTimeSeries
import time 


p = PersistTimeSeries.PersistTimeSeries()
while True: 
    p.persist_battery_level()
    time.sleep(30)