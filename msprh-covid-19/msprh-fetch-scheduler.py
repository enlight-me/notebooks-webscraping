# -*- coding: utf-8 -*-
# © 2020 BENAHMED DAHO Ali
# © 2020 Enlight.ms (<https://enlightme.biz>)
# License Apache-2.0 (http://www.apache.org/licenses/).

from datetime import datetime
import time
import requests
import json
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler

########################################################################################################
# fetch_covid19_cumul_dz
#

def fetch_covid19_cumul_dz():

    now = datetime.now()
    fetch_date = now.strftime("%d-%m-%Y-%H-%M-%S")

    # Define the request URL
    base_url_cumul = 'https://services8.arcgis.com/yhz7DEAMzdabE4ro/arcgis/rest/services/COVID_Death_Cumul/FeatureServer/2/query?'

    params_cumul = {'f': 'json', 'where': '1=1', 'returnGeometry': 'false', 'spatialRel': 'esriSpatialRelIntersects',
            'outFields': '*', 'orderByFields': 'Report asc', 'outSR': '102100', 'resultOffset': '0',
            'resultRecordCount': '1000', 'cacheHint': 'true'}

    # Send the request
    cumul_global_response = requests.get(base_url_cumul, params_cumul)

    if (cumul_global_response.ok == False):
        exit()

    # Create a python variable from the json
    cumul_global = cumul_global_response.json()

    # cumul_global_json = json.dumps(cumul_global, indent = 4)
    # print(cumul_global['features'])

    new_cases = [(w['attributes']) for w in cumul_global['features']]

    # for case in new_cases: 
    #     print(case['Report'], case['Cumul'], case['gueris'])

    # Create a pandas object

    df = pd.DataFrame(new_cases)

    df_to_save = df[['Cumul' , 'Death_cumul', 'Féminin' , 'Masculin' , 'NP' , 'New_cases', 'Reanim' , 'Report' , 'Straitem' , 'Testnegatif' , 'Testpositif' , 'an' , 'cinquanteneuf' , 'gueris' , 'quaranteneuf' , 'soixante' , 'unquatorze' , 'vingtquatre']]

    # print (df)

    # Write to a file 

    df_to_save.to_csv(save_dir + 'covid19-cumul-dz-'+fetch_date+'.csv', index = False, header = True)

########################################################################################################
# fetch_covid19_stats_wilayas_dz
#

def fetch_covid19_stats_wilayas_dz():
    
    now = datetime.now()
    fetch_date = now.strftime("%d-%m-%Y-%H-%M-%S")

    # Define the request URL
    base_url_wilayas = 'https://services8.arcgis.com/yhz7DEAMzdabE4ro/arcgis/rest/services/Cas_confirme_view/FeatureServer/0/query?'

    params_wilayas = {'f': 'json', 'where': '1=1', 'returnGeometry': 'false', 'spatialRel': 'esriSpatialRelIntersects',
            'outFields': '*', 'orderByFields': 'Cas_confirm desc', 'outSR': '102100', 'resultOffset': '0',
            'resultRecordCount': '48', 'cacheHint': 'true'}

    # Send the request
    wilayas_response = requests.get(base_url_wilayas, params_wilayas)

    if (wilayas_response.ok == False):
        exit()

    # Create a python variable from the json
    wilayas = wilayas_response.json()

    wilayas_stats = [(w['attributes']) for w in wilayas['features']]

    # print (wilayas_stats[0])
    
    # Create a pandas object

    df_wilayas = pd.DataFrame(wilayas_stats)


    df_wilayas_to_save = df_wilayas[["WILAYA", "NOM_WILAYA", "wilayat", "Cas_confirm" , "Décés" , "Récupér" , "active" , "Femelle", "Males", 
                                "A1_25", "a25_34", "a35_44", "a45_59", "A_60", "Date_rapport"]]

    # print (df_wilayas_to_save)

    # Write to a file 

    df_wilayas_to_save.to_csv(save_dir + 'covid19-wilayas-dz-'+fetch_date+'.csv', index = False, header = True)

########################################################################################################
# Main
#

# The base directory to save files in
save_dir = '/home/username/datasets/msprh-covid-19'

# Main loop sleeping time in seceonds
loop_sleeping_time = 60

if __name__ == "__main__":

    scheduler = BackgroundScheduler(daemon=True)

    # intervals can be : minutes, days
    scheduler.add_job(fetch_covid19_cumul_dz, 'interval', minutes=1, id='covid19_cumul')

    scheduler.add_job(fetch_covid19_stats_wilayas_dz, 'interval', minutes=1, id='covid19_wilayas')

    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(loop_sleeping_time)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()    
