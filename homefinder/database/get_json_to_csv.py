import json
import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="JSON file name")
args = parser.parse_args()
file_name = os.path.splitext(args.json_file)[0]

with open(file_name+'.json', 'r') as f:
    data = json.load(f)

image_csv_data = []
propert_csv_data = []
agent_csv_data = []

for i in range(len(data['properties'])):
    temp_property = data['properties'][i]
    property_data = {}
    property_id = i + 100
    property_data['property_id'] = property_id
    property_data['property_name'] = temp_property['address1'] + ' ' + temp_property['address2']
    property_data['description'] = temp_property['description']
    property_data['num_bedroom'] = temp_property['beds']['count']
    property_data['num_bathroom'] = temp_property['baths']['count']
    property_data['area_size'] = temp_property['sqft']
    property_data['price'] = temp_property['price'][1:]
    property_data['transaction_type'] = 'Buy'
    property_data['property_type'] = 'House'
    property_data['parking'] = 'garage'
    property_data['laundry'] = 'in_suite'
    property_data['furnished'] = True
    property_data['pet_friendly'] = True
    property_data['latitude'] = temp_property['lat']
    property_data['longitude'] = temp_property['lon']
    property_data['build_year'] = temp_property['yearBuilt']
    property_data['smoking_allowed'] = False
    property_data['air_conditioning'] = False
    property_data['hardwood_floors'] = True
    property_data['balcony'] = True
    propert_csv_data.append(property_data)

propert_csv_data = pd.DataFrame.from_records(propert_csv_data)

propert_csv_data.to_csv(file_name+'.csv')