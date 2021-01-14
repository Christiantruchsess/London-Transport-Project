# Import required packages
import requests as re
import json
import pprint as pp
import os

# Define variables for helper functions
app_id = os.environ['LONDON_TRANSPORT_PRIMARY_KEY']
app_key = os.environ["LONDON_TRANSPORT_SECONDARY_KEY"]
url_append = f'?app_id={app_id}&app_key={app_key}' 

# "load" required APIs
air_quality_url = "https://api.tfl.gov.uk/AirQuality"
modes_of_transport_url = "https://api.tfl.gov.uk/Line/Meta/Modes"
bike_points_url = "https://api.tfl.gov.uk/BikePoint"
tube_lines_url = 'https://api.tfl.gov.uk/Line/Mode/tube'
bus_lines_url ='https://api.tfl.gov.uk/Line/Mode/bus'

# Define helper function
def response_maker(api_url,param1,param2):
    return(re.get(api_url+url_append, params={param1:param2}).json())

# Define main functions
def air_quality():
    print('Enter 0 if you want the air quality forecast for today, or 1, if you want it for tomorrow: ')
    day = int(input())
    air_quality_response = response_maker(air_quality_url,'','')
    print('\n')
    pp.pprint(air_quality_response['currentForecast'][day]['forecastText'])
    print('\nI\'m sorry the formatting is so ugly... It\'s the API\'s fault!!! I promise my programmer will fix it later...\n')

def modes_transport():
    modes_response = response_maker(modes_of_transport_url,'','')
    modes_list = [i['modeName'] for i in modes_response]
    print(f'According to Transport for London, there are {len(modes_list)} modes of transport available in the city, which you can see listed below:\n')
    print(str(modes_list), '\n')

def bike_points():
    bikes_response = response_maker(bike_points_url,'','')
    total_docks = 0
    for i in range(len(bikes_response)):
        total_docks += int(bikes_response[i]['additionalProperties'][-1]['value'])
    print(f'In the city, there are {len(bikes_response)} BikePoints operated by Transport for London.\n')
    print(f'Combined, all the BikePoints amount to exactly {total_docks} bike docks in total! It\'s not at Amsterdam\'s level, but still, pretty impressive!\n')

def tube_bus_lines():
    tube_lines_response = response_maker(tube_lines_url,'','')
    bus_lines_response = response_maker(bus_lines_url,'','')
    tube_name_list = []
    for i in range(len(tube_lines_response)):
        tube_name_list.append(tube_lines_response[i]['name'])
    print(f'There are {len(bus_lines_response)} bus lines in London, as well as {len(tube_lines_response)} lengthy tube lines listed below:\n')
    print(tube_name_list,'\n')

def num_tube_stations():
    print('In fact, if you input which tube line you are interested in, I will tell you how many stations it has and list them out for you:\n')
    line = input()
    tube_stations_url = f'https://api.tfl.gov.uk/Line/{line}/StopPoints'
    tube_stations_response = response_maker(tube_stations_url,'','')
    station_list = []
    for i in range(len(tube_stations_response)):
        station_list.append(tube_stations_response[i]['commonName'])
    print(f'There are {len(tube_stations_response)} stations on the {line} line:\n\n', station_list, '\n')

def journey_times():
    print('...and now, my greatest feature! If you want to travel from one point to another in London, just give me the corresponding postal codes,\n\
and I\'ll tell you whether the tube or the bus is quicker (If you have no idea what to input...\
Heathrow International Airport\'s postal code is Tw61RU, and Tower Bridge\'s is SE14TW).\n')
    print('Postal code of ORIGIN: ')
    postal_code1 = input()
    print('\n')
    print('Postal code of DESTINATION: ')
    postal_code2 = input()
    print('\n')
    journey_url = f"https://api.tfl.gov.uk/Journey/JourneyResults/{postal_code1}/to/{postal_code2}"
    bus_journey_response = response_maker(journey_url,'mode','bus')
    tube_journey_response = response_maker(journey_url,'mode','tube')
    bus_minutes = min([i['duration'] for i in bus_journey_response['journeys']])
    tube_minutes = min([i['duration'] for i in tube_journey_response['journeys']])
    
    print(f'The bus ride will take you {bus_minutes} minutes.\n')
    print(f'The tube ride will take you {tube_minutes} minutes.\n')
    if bus_minutes < tube_minutes:
        print('You should take the bus, it\'s obviously faster.')
    else:  
        print('You should take the tube, it\'s obviously faster.')

# Write introduction text
print("\nHello there! I may look like software straight out of the 80s, but I can actually help you out a little bit.\n\
\nI have a few tricks up my sleeve... I can use the \"Transport for London\" APIs in order to fetch relevant information on the city:\n")

# Call functions
air_quality()
modes_transport()
bike_points()
tube_bus_lines()
num_tube_stations()
journey_times()

# Write goodby text
print('\nThat is all. Thank you!')