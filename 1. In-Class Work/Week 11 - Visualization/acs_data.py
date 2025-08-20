from requests import get

import numpy as np 
import pandas as pd 

def get_county_data(year, census_key):
    '''
    Gets county-level data from the ACS using the Census API
    
    Arguments:
        year: Year for which the data should be pulled
        census_key: str, the Census key to use to pull from the API
        
    Returns:
        A DataFrame
    '''
    census_base_url = f'https://api.census.gov/data/{year}/acs/acs1/profile'

    census_params = {'get':'NAME,DP02_0001E,DP03_0087E,DP03_0002PE,DP02_0068PE,DP02_0066PE',
                     'for':'county:*',
                     'key': census_key}

    r = get(census_base_url, params = census_params)
    people_by_county = r.json()
    
    # Get the data into dictionary format
    keys = ['county', 'num_households','mean_income','percent_employed','percent_bachelors','percent_graduate']

    census_dict = {key:[county[keys.index(key)] for county in people_by_county[1:]] for key in keys}
    census_df = pd.DataFrame(census_dict)
    
    # Change numeric values to numeric
    census_df[keys[1:]] = census_df[keys[1:]].apply(pd.to_numeric)
    census_df['state'] = [i[1] for i in census_df.county.str.split(', ')]
    return census_df

def get_us_data(year, census_key):
    '''
    Gets US-level data from the ACS using the Census API
    
    Arguments:
        year: Year for which the data should be pulled
        census_key: str, the Census key to use to pull from the API
        
    Returns:
        A DataFrame
    '''
        
    census_base_url = f'https://api.census.gov/data/{year}/acs/acs1/profile'

    census_params = {'get':'NAME,DP02_0001E,DP03_0087E,DP03_0002PE,DP02_0068PE,DP02_0066PE',
                     'for':'us:1',
                     'key': census_key}

    r = get(census_base_url, params = census_params)
    people_by_county = r.json()
    
    # Get the data into dictionary format
    keys = ['US', 'num_households','mean_income','percent_employed','percent_bachelors','percent_graduate']

    census_dict = {key:[county[keys.index(key)] for county in people_by_county[1:]] for key in keys}
    census_df = pd.DataFrame(census_dict)
    
    # Change numeric values to numeric
    census_df[keys[1:]] = census_df[keys[1:]].apply(pd.to_numeric)
    
    return census_df