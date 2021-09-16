# MapQuest_input.py
#
# ICS 32 Spring 2018
#Name: Eric Liu
#StudentID: 56277704

import json
import urllib.parse
import urllib.request

MAPQUEST_API_KEY = 'EEYATeFm3SqnUekqqOnMPrrwLWD2Gl0r'

BASE_MAPQUEST_URL = 'http://open.mapquestapi.com'

def build_route_url(locations: [str]) -> str:
    '''
    This function takes a list of locations,
    and builds and returns a URL that can be used to ask the
    MAPQUEST API for information about route.
    '''
    route_parameters = [
        ('key', MAPQUEST_API_KEY), ('from', locations[0]),
    ]

    for i in range(1, len(locations)):
        route_parameters.append(('to',locations[i]))

    return BASE_MAPQUEST_URL + '/directions/v2/route?' + urllib.parse.urlencode(route_parameters)

def build_elevation_url(latitude_longitude: str) -> str:
    '''
    This function takes  latitude and longitude strings,
    and builds and returns a URL that can be used to ask the
    MAPQUEST API for information about elevation.
    '''

    elevation_parameters = [
        ('key', MAPQUEST_API_KEY), ('latLngCollection', latitude_longitude),
        ('unit', 'f')
    ]

    return BASE_MAPQUEST_URL + '/elevation/v1/profile?' + urllib.parse.urlencode(elevation_parameters)

def get_result(url: str) -> dict:
    '''
    This function takes a URL and returns a Python dictionary representing the
    parsed JSON response.
    '''
    response = None

    try:
        response = urllib.request.urlopen(url)
        json_text = response.read().decode(encoding = 'utf-8')

        return json.loads(json_text)
    except:
        print('\nMAPQUEST ERROR')
    finally:
        if response != None:
            response.close()
