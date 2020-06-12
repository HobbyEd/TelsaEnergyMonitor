import persist_time_series_for_tesla as persist_tesla
import time 


p = persist_tesla.PersistTimeSeriesForTesla()
while True: 
    p.persist_vehicles_state()
    time.sleep(100)