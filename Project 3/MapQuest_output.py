# MapQuest_output.py
#
# ICS 32 Spring 2018
#Name: Eric Liu
#StudentID: 56277704

import MapQuest_input

class Steps:
    '''
    a class for step-by-step directions
    the show function returns the directions
    '''

    def show(self, json_response):
        print('DIRECTIONS')
        for legs in json_response['route']['legs']:
            for maneuvers in legs['maneuvers']:
                print(maneuvers['narrative'])
        print()

class Total_Distance:
    '''
    a class for the total distance traveled if completing the entire trip
    the show function returns the total distance
    '''

    def show(self, json_response):
        distance = round(json_response['route']['distance'])
        print('TOTAL DISTANCE: {} miles'.format(distance))
        print()

class Total_Time:
    '''
    a class for the total estimated time to complete the entire trip
    the show function returns the total estimated time
    '''

    def show(self, json_response):
        time = round(json_response['route']['time']/60)
        print('TOTAL TIME: {} minutes'.format(time))
        print()

class Lat_Long:
    '''
    a class for the latitude and longitude of each of the locations specified in the input
    the show function returns the latitude and longitude
    '''

    def show(self, json_response):
        print('LATLONGS')
        for latlng in json_response['route']['locations']:
            latitude = latlng['displayLatLng']['lat']
            longitude = latlng['displayLatLng']['lng']
            if latitude < 0:
                print('{:.2f}S'.format(abs(latitude)), end=' ')
            else:
                print('{:.2f}N'.format(abs(latitude)), end=' ')
            if longitude < 0:
                print('{:.2f}W'.format(abs(longitude)))
            else:
                print('{:.2f}E'.format(abs(longitude)))
        print()

class Elevation:
    '''
    a class for the elevation, in feet, of each of the locations specified in the input
    the show function returns the elevation
    '''

    def show(self, json_response):
        print('ELEVATIONS')
        elevation_data = _get_elevation(json_response)
        for data in elevation_data:
            print(data)
        
def _get_elevation(json_response: 'json') -> [int]:
    '''
    this function takes in json response, and returns
    a list of integer of the elevation
    '''
    elevation_list = []
    latlng_list = []
    for latlng in json_response['route']['locations']:
            latlng_list.append(latlng['displayLatLng']['lat'])
            latlng_list.append(latlng['displayLatLng']['lng'])
    for i in range(0,len(latlng_list),2):
        latlng_str = '{},{}'.format(str(latlng_list[i]),str(latlng_list[i+1]))
        elevation_data = MapQuest_input.get_result(MapQuest_input.build_elevation_url(latlng_str))
        for data in elevation_data['elevationProfile']:
            elevation_list.append(round(data['height']))
    return elevation_list
