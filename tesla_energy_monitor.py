import persist_time_series as PersistTimeSeries
import time 


p = PersistTimeSeries.PersistTimeSeries()
while True: 
    p.persist_vehicles_state()
    time.sleep(5)