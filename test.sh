from google.cloud import bigquery
import pandas as pd
from tqdm import tqdm
from pathlib import Path

"""BIG QUERY FUNCTIONS"""

def client():
    """require a bigquery project and credentials, save in json in root main directory"""
    credsfile = Path().resolve().joinpath('antiechochambers-1ba7f7f4c68e.json')
    return bigquery.Client.from_service_account_json(credsfile)

def jobConfig():
    config = bigquery.QueryJobConfig()
    config.query_parameters = (bigquery.ScalarQueryParameter('size', 'INT64', 10),)
    config.use_legacy_sql = False
    config.maximum_bytes_billed = int(5e9)
    
    return config

def run_job(query):
    print('Submitting query')
    j = client().query(query=query, job_config=jobConfig())
    with tqdm() as pbar:
        while True:
            try:
                j.result(timeout=1)
            except TimeoutError:                
                pbar.update(1)
            else:
                break
    return j

def fetchQuery(query):
    j = run_job(query)
    df = j.to_dataframe()
    
    return df

def fetchSubList():
    """should create bot table to call on"""
    query = f"""SELECT *
                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.randomSubreddits`
                 """

    data = fetchQuery(query)
    
    return data
    
sublist = fetchSubList()
print(sublist.shape)