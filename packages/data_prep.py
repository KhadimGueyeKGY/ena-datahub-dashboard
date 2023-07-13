import os
import requests
import datetime
import io
import pandas as pd
import getpass
from requests.auth import HTTPBasicAuth

'''ena_searches = {
    'analysis': {
        'search_fields': ['analysis_accession', 'analysis_title', 'analysis_type', 'study_accession', 'study_title', 'sample_accession', 'center_name', 'first_public', 'first_created', 'tax_id', 'scientific_name', 'pipeline_name', 'pipeline_version', 'country', 'collection_date'],
        'result_type': 'analysis',
        'data_portal': 'pathogen',
        'authentication': 'True'
    },
    'read_run': {
        'search_fields': ['experiment_accession', 'study_accession', 'study_title', 'sample_accession', 'experiment_title', 'country', 'collection_date', 'center_name', 'broker_name', 'tax_id', 'scientific_name', 'instrument_platform', 'instrument_model', 'library_layout', 'library_name', 'library_selection', 'library_source', 'library_strategy', 'first_public', 'first_created'],
        'result_type': 'read_run',
        'data_portal': 'pathogen',
        'authentication': 'True'
    }
    
}
'''
class GetData :
    ena_searches = {
        'analysis': {
            'search_fields': ['analysis_accession', 'analysis_title', 'analysis_type', 'study_accession', 'study_title', 'sample_accession', 'center_name', 'first_public', 'first_created', 'tax_id', 'scientific_name', 'pipeline_name', 'pipeline_version', 'country', 'collection_date'],
            'result_type': 'analysis',
            'data_portal': 'pathogen',
            'authentication': 'True'
        },
        'read_run': {
            'search_fields': [ 'country', 'first_created',  'broker_name',  'instrument_platform', 'instrument_model','center_name'],
            'result_type': 'read_run',
            'data_portal': 'pathogen',
            'authentication': 'True'
        }
        
    }

    BASE_PORTAL_API_SEARCH_URL = 'https://www.ebi.ac.uk/ena/portal/api/search'

    def __init__(self):
        pass
    def get_url(data_type):
        url = ''.join([
            GetData.BASE_PORTAL_API_SEARCH_URL,
            '?',
            'dataPortal=' + data_type['data_portal'],
            '&',
            'fields=' + '%2C'.join(data_type['search_fields']),
            '&',
            'result=' + data_type['result_type'],
            '&dccDataOnly=True&limit=0'
        ])
        return url

    def authentication():
        username = ''
        password = ''
        try : 
            authentication = pd.read_csv('authentication.tsv',sep = '\t')
            password = str(authentication['password'][0])
            username = str(authentication['username'][0])
        except :
            username = ''
            password = ''
        while (username == '') and (password == ''):
            username = input('Username => ')
            password = getpass.getpass(prompt='Password => ')
        return username , password
    
    def authentication_1():
        username = ''
        password = ''
        while (username == '') and (password == ''):
            username = input('Username => ')
            password = getpass.getpass(prompt='Password => ')
        return username , password

    def main (username , password):
        data_analysis = []
        data_read_run = []
        if username=='' or password =='nan' or username=='nan' or password =='' :
            username , password = GetData.authentication_1()
        for i in GetData.ena_searches:
            print('> Running data request: {} ... [{}]'.format(i, datetime.datetime.now()))
            url = GetData.get_url(GetData.ena_searches[i])
            response = requests.get(url,auth=HTTPBasicAuth(username, password))
            data = pd.read_csv(io.StringIO(response.content.decode('UTF-8')), sep="\t",low_memory=False)
            data = data.fillna('-1')
            if i == 'analysis':
                data_analysis = data
            else:
                data_read_run = data
            #data.to_csv('packages/data/{}_ENA_Search_{}.csv'.format(username,i), index=False)  
            #os.system('curl "{}" --output data/{}_ENA_Search_{}.csv'.format(url,username,i))
            print('> Running data request: {} ... [DONE] [{}]'.format(i, datetime.datetime.now()))
        return data_analysis , data_read_run


