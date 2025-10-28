import requests
from requests.models import PreparedRequest
import time
import pandas as pd


# a function to parse a response from the members endpoint
def member_parser(response):
    """This function would parse the results from a query to the members endpoint."""
    members_json = response.json()['members']
    member = [{'bioguideId' : i.get('bioguideId'),
              'district' : i.get('district'),
              'name' : i.get('name'),
              'partyName' : i.get('partyName'),
              'state': i.get('state'),
              'chamber':i.get('terms').get('item')[-1].get('chamber'),
              'startYear':i.get('terms').get('item')[-1].get('startYear'),
              'endYear':i.get('terms').get('item')[-1].get('endYear'),
              'url' : i.get('url')} for i in members_json]
    member_frame = pd.DataFrame(member)
    return member_frame

# a function that paginates over all pages
def congress_paginate(initial_url, params):
    """Takes an initial URL and a list of parameters for the Congress.gov API and automitically paginates the results"""
    # remove the API key from the parameters list 
    apikey = params.pop('api_key')
    req = PreparedRequest()
    req.prepare_url(initial_url, params) # prep a url
    nextpage = req.url 
    responses_list = []
    # iterate over next page URLs
    while nextpage!=None:
        nextpage_url = nextpage + '&api_key=' + apikey
        response = requests.get(nextpage_url)
        responses_list.append(response)
        nextpage = response.json().get('pagination').get('next')
        time.sleep(5000/3600)
    return responses_list