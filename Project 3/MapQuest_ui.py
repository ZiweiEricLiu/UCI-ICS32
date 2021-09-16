# MapQuest_ui.py
#
# ICS 32 Spring 2018
#Name: Eric Liu
#StudentID: 56277704

import MapQuest_input
import MapQuest_output

def ask_for_locations() -> [str]:
    '''
    ask the user for number of locations
    and the names of locations
    return a list of locations
    '''
    location_list = []
    number_of_locations = int(input())
    for i in range(number_of_locations):
        location = input()
        location_list.append(location)
    return location_list

def ask_for_desired_output() -> [str]:
    '''
    ask the user for number of desired outputs
    and the desired outputs
    return a list of desired outputs
    '''
    desired_outputs_list = []
    number_of_desired_outputs = int(input())
    for i in range(number_of_desired_outputs):
        desired_outputs = input()
        desired_outputs_list.append(desired_outputs)
    return desired_outputs_list

def creat_output_list(desired_outputs: [str]) -> [str]:
    '''
    this function takes in a list of desired outputs
    and returns a list of desired outputs' objects
    '''
    output_list = []
    for outputs in desired_outputs:
        if outputs == 'STEPS':
            output_list.append(MapQuest_output.Steps())
        elif outputs == 'TOTALDISTANCE':
            output_list.append(MapQuest_output.Total_Distance())
        elif outputs == 'TOTALTIME':
            output_list.append(MapQuest_output.Total_Time())
        elif outputs == 'LATLONG':
            output_list.append(MapQuest_output.Lat_Long())
        elif outputs == 'ELEVATION':
            output_list.append(MapQuest_output.Elevation())
    return output_list

if __name__ == '__main__':
    location_list = ask_for_locations()
    desired_outputs_list = ask_for_desired_output()
    output_list = creat_output_list(desired_outputs_list)
    json_response = MapQuest_input.get_result(MapQuest_input.build_route_url(location_list))
    print()
    if json_response['route']['routeError']['errorCode'] != -400:
        print('NO ROUTE FOUND')
    else:
        for output in output_list:
            output.show(json_response)
        print()
        print('Directions Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors')
