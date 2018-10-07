start startInflux.bat
timeout 10 > NULL
start startTelegraf.bat 
timeout 3 > NULL
start startGrafana.bat 
timeout 3 > NULL
start startTimeSerie.bat 