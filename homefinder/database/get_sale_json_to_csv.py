import json
import pandas as pd
import os
import argparse
import random

parser = argparse.ArgumentParser()
parser.add_argument("json_file", help="JSON file name")
args = parser.parse_args()
file_name = os.path.splitext(args.json_file)[0]

with open(file_name+'.json', 'r') as f:
    data = json.load(f)

image_csv_data = []
propert_csv_data = []

for i in range(len(data['properties'])):
    temp_property = data['properties'][i]
    property_data = {}
    property_id = i + 1000*int(file_name.split('_')[-1])
    property_data['property_id'] = property_id
    property_data['property_name'] = temp_property['address1'] + ' ' + temp_property['address2']
    property_data['description'] = temp_property['description']
    property_data['num_bedroom'] = temp_property['beds']['count']
    property_data['num_bathroom'] = temp_property['baths']['count']
    property_data['area_size'] = temp_property['sqft']
    property_data['price'] = temp_property['price'][1:].replace(',', '')
    property_data['transaction_type'] = 'Buy'
    property_data['property_type'] = random.choice(['Apartment', 'Townhouse', 'Condo Unit', 'House', 'Duplex'])
    property_data['parking'] = random.choice(['garage', 'underground', 'covered', 'outdoor'])
    property_data['laundry'] = random.choice(['in_suite', 'shared'])
    property_data['furnished'] = random.choice([True, False])
    property_data['pet_friendly'] = True
    property_data['latitude'] = temp_property['lat']
    property_data['longitude'] = temp_property['lon']
    property_data['build_year'] = temp_property['yearBuilt']
    property_data['smoking_allowed'] = False
    property_data['air_conditioning'] = random.choice([True, False])
    property_data['hardwood_floors'] = random.choice([True, False])
    property_data['balcony'] = random.choice([True, False])

    property_data['agent_name'] = temp_property['agent']['name']
    property_data['agent_phone'] = temp_property['office']['phone']
    property_data['agent_email'] = '_'.join(temp_property['agent']['name'].split(' '))+'@gmail.com'
    
    propert_csv_data.append(property_data)

    image_data = {}
    image_data['image_id'] = property_id
    image_data['image_url'] = temp_property['photos']['url']
    image_data['property_id'] = property_id
    image_data['image_type'] = random.choice(['indoor', 'outdoor'])
    image_csv_data.append(image_data)

propert_csv_df = pd.DataFrame.from_records(propert_csv_data)
propert_csv_df.to_csv(file_name+'_property.csv')

image_csv_df = pd.DataFrame.from_records(image_csv_data)
image_csv_df.to_csv(file_name+'_image.csv')
