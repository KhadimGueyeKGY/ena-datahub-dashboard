# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 17:36:18 2023

@author: khadim
"""
# import geopandas as gpd
import pandas as pd
import plotly.express as px
import json




#   list of capital : lat and lon https://www.kaggle.com/datasets/nikitagrec/world-capitals-gps?resource=download

class geoM:
    def __init__(self):
        init = 0 
    def contry_lon_lat(ContryInput):
        df_2 = {'CountryName':[],'ContinentName':[],'CapitalLatitude':[],'CapitalLongitude':[],'size':[]}
        #### data prep
        for i in range(len(ContryInput)):
            if ':' in ContryInput[i]:
                ContryInput[i] = ContryInput[i].split(':')[0]
        ContryInput_U = list(set(ContryInput)- {''})
        df_2['size'] = [ContryInput.count(i) for i in ContryInput_U ]
        ### refe read 
        ContinentContry = pd.read_csv("assets/concap.csv")
        ContinentName = list(ContinentContry["ContinentName"])
        CountryName = list(ContinentContry["CountryName"])
        # CapitalName = list(ContinentContry["CapitalName"])
        CapitalLatitude = list(ContinentContry["CapitalLatitude"])
        CapitalLongitude = list(ContinentContry["CapitalLongitude"])
        # CountryCode = list(ContinentContry["CountryCode"])
        for i in range(len(ContryInput)) :
            for j in range(len(CountryName)):
                if str(CountryName[j].lower()).find(str(ContryInput[i]).lower()) != -1 :
                    df_2['CountryName'].append(CountryName[j])
                    df_2['ContinentName'].append(ContinentName[j])
                    df_2['CapitalLatitude'].append(CapitalLatitude[j])
                    df_2['CapitalLongitude'].append(CapitalLongitude[j])
                    break
            if j == len(CountryName) -1 :
                if str(ContryInput[i]).find(',') != -1 : 
                    nwc = str(ContryInput[i]).replace(',', '')
                else:
                    nwc = str(ContryInput[i])
                if nwc.find(" ") != -1:
                    CI = nwc.split(" ")
                    for j in range(len(CountryName)):
                        for o in range(len(CI)):
                            if str(CountryName[j].lower()).find(CI[o].lower()) == -1 :
                                df_2['CountryName'].append(CountryName[j])
                                df_2['ContinentName'].append(ContinentName[j])
                                df_2['CapitalLatitude'].append(CapitalLatitude[j])
                                df_2['CapitalLongitude'].append(CapitalLongitude[j])
                                break
                    if j ==len(CountryName) -1 : 
                        df_2['CountryName'].append(ContryInput[i])
                        df_2['ContinentName'].append('')
                        df_2['CapitalLatitude'].append(0)
                        df_2['CapitalLongitude'].append(0)
                else :
                    df_2['CountryName'].append(ContryInput[i])
                    df_2['ContinentName'].append('')
                    df_2['CapitalLatitude'].append(0)
                    df_2['CapitalLongitude'].append(0)
        for i in range(len(df_2['CountryName'])):
            df_2['size'].append(df_2['CountryName'].count(df_2['CountryName'][i]))
        return pd.DataFrame(df_2)

    
    def map(data):
        print('yup')
        data_2 = geoM.contry_lon_lat(list(data['country'])) 
        #new_data = pd.concat([data,data_2],axis=1)
        new_data = data_2
        print('oki')
        px.set_mapbox_access_token('pk.eyJ1Ijoia2hhZGltZ3VleWVrZ3kiLCJhIjoiY2xiM3BsMnBpMGhhZTNvb2Exc3B5eHl6OCJ9.lA_AUaGIJxDHLjaokBbxDg')
        fig = px.scatter_mapbox(new_data,
                                lat='CapitalLatitude',
                                lon='CapitalLongitude',
                                #color=color,
                                size="size",
                                size_max=15,
                                hover_name="CountryName",
                                height = 1000,
                                zoom=2)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig
    
    def df_map(ContryInput): # for Choropleth_map
        df = {'code':[],'size':[]}
        #### data prep
        for i in range(len(ContryInput)):
            if ':' in str(ContryInput[i]):
                ContryInput[i] = ContryInput[i].split(':')[0]
        ContryInput_U = list(set(ContryInput)- {'-1'})
        del ContryInput_U[ContryInput_U.index('missing')]
        df['size'] = [ContryInput.count(i) for i in ContryInput_U ]
        code_3 = pd.read_csv('assets/Officially_assigned_code_elements.csv',sep= '\t')
        for i in ContryInput_U :
            for j in range(len(code_3.country)) : 
                if str(code_3.country[j].lower()).find(i.lower()) != -1  :
                    df['code'].append(code_3.code[j])
                    break
            if j == len(code_3.country) -1:
                print(str(i) + ' not found !!!')
        #print(df['code'])
        #print(len(df['code']))
        #print (pd.DataFrame(df))
        return pd.DataFrame(df)

    def Choropleth_map(data, default_color='gray'): # Input as a data frame containing two columns, code 3 and the size   
        with open('assets/geojson-counties-fips.json') as response:
            counties = json.load(response)
        px.set_mapbox_access_token('pk.eyJ1Ijoia2hhZGltZ3VleWVrZ3kiLCJhIjoiY2xiM3BsMnBpMGhhZTNvb2Exc3B5eHl6OCJ9.lA_AUaGIJxDHLjaokBbxDg')
        fig = px.choropleth_mapbox(data, geojson=counties, locations='code', color='size',
                           color_continuous_scale="blues",
                           range_color=(min(list(data['size']))-1, max(list(data['size']))-1),
                           mapbox_style="carto-positron",
                           zoom=1, center = {"lat": 15.372460769473202, "lon": -16.48902546251731},   # 15.372460769473202, -16.48902546251731
                           opacity=0.5,
                           labels={'pays':'unemployment rate'},
                           #hover_template='%{hovertext}<br>Size: %{customdata[0]}',
                           hover_data={'size': True},
                           hover_name='code',
                          )
        fig.update_traces(marker_color=default_color, selector={'location': ''})

        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=650,)
        return fig
    


