import requests 
from requests.auth import HTTPBasicAuth
import xmltodict  

class Smile: 
    def __init__(
        self,
        host,
        password,
        username="smile",
        port=80,
        ):
        self._endpoint = f"http://{host}:{str(port)}/core/domain_objects"
        self._password = password 
        self._username = username 
        self._actueel_opgewekt = {}
        self._actueel_verbruikt = {}
        self._cumulatief_opgewekt_laag_tarief = {}
        self._cumulatief_opgewekt_hoog_tarief = {}
        self._cumulatief_verbuikt_laag_tarief = {}
        self._cumulatief_verbuikt_hoog_tarief = {}

    def get_actueel_opgewekt(self): 
        return self._actueel_opgewekt

    def get_actueel_verbruikt(self):
        return self._actueel_verbruikt

    def get_cumulatief_verbuikt_hoog_tarief(self): 
        return self._cumulatief_verbuikt_hoog_tarief
    
    def get_cumulatief_verbuikt_laag_tarief(self): 
        return self._cumulatief_verbuikt_laag_tarief

    def get_cumulatief_opgewekt_hoog_tarief(self): 
        return self._cumulatief_opgewekt_hoog_tarief

    def get_cumulatief_opgewekt_laag_tarief(self): 
        return self._cumulatief_opgewekt_laag_tarief

    def update_data(self):
        resp = requests.get(self._endpoint, auth=HTTPBasicAuth(self._username, self._password) )
        resp_dict = xmltodict.parse(resp.content)

        # Zet alle actuele waarden.        
        for verbruik in resp_dict['domain_objects']['module']['services']['electricity_point_meter']['measurement']:
            if verbruik['@directionality'] == 'consumed': 
                self._actueel_verbruikt = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
            elif verbruik['@directionality'] == 'produced':
                self._actueel_opgewekt = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
        
        #Zet alle cumulatieve waarden. 
        for verbruik in resp_dict['domain_objects']['module']['services']['electricity_cumulative_meter']['measurement']:
            if verbruik['@directionality'] == 'consumed': 
                if verbruik['@tariff_indicator'] == 'nl_peak':
                    self._cumulatief_verbuikt_hoog_tarief = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
                elif verbruik['@tariff_indicator'] == 'nl_offpeak':
                    self._cumulatief_verbuikt_laag_tarief = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
            elif verbruik['@directionality'] == 'produced':
                if verbruik['@tariff_indicator'] == 'nl_peak':
                    self._cumulatief_opgewekt_hoog_tarief = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}
                elif verbruik['@tariff_indicator'] == 'nl_offpeak':
                    self._cumulatief_opgewekt_laag_tarief = {'waarde': verbruik['#text'], "time_stamp": verbruik['@log_date'], "eenheid": verbruik['@unit']}



p1 = Smile('192.168.86.31','mqjccbtf') 
p1.update_data()
print ("toppie")
