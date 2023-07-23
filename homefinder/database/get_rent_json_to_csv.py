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
agent_csv_data = []

for i in range(len(data['listings'])):
    temp_property = data['listings'][i]
    property_data = {}
    property_data['property_id'] = temp_property['ref_id']
    property_data['property_name'] = temp_property['title'] if 'title' in temp_property.keys() else temp_property['intro']
    property_data['description'] = temp_property['intro']
    if 'beds' in temp_property.keys():
        if temp_property['beds'] == 'studio':
            property_data['num_bedroom'] = 1
        else:
            property_data['num_bedroom'] = str(float(temp_property['beds'][0])+0.5) if 'den' in temp_property['beds'] else temp_property['beds']
    else:
        property_data['num_bedroom'] = '1'
    property_data['num_bathroom'] = temp_property['baths'] if 'baths' in temp_property.keys() else '0'
    property_data['area_size'] = temp_property['sq_feet'] if 'sq_feet' in temp_property.keys() else '0'
    property_data['price'] = temp_property['price']
    property_data['transaction_type'] = 'Rent'
    property_data['property_type'] = temp_property['type']
    property_data['parking'] = random.choice(['garage', 'underground', 'covered', 'outdoor'])
    property_data['laundry'] = random.choice(['in_suite', 'shared'])
    property_data['furnished'] = random.choice([True, False])
    if 'dogs' not in temp_property.keys():
        temp_property['dogs'] = 0
    if 'cats' not in temp_property.keys():
        temp_property['cats'] = 0
    property_data['pet_friendly'] = True if temp_property['dogs'] + temp_property['cats']  > 0 else False
    property_data['latitude'] = temp_property['latitude']
    property_data['longitude'] = temp_property['longitude']
    property_data['build_year'] = temp_property['a']
    property_data['smoking_allowed'] = False
    # property_data['water'] = True if 'Water' in temp_property['utilities_included'] else False
    # property_data['heat'] = True if 'Heat' in temp_property['utilities_included'] else False
    property_data['air_conditioning'] = random.choice([True, False])
    property_data['hardwood_floors'] = random.choice([True, False])
    property_data['balcony'] = random.choice([True, False])
    propert_csv_data.append(property_data)

    image_data = {}
    image_data['image_id'] = temp_property['ref_id']
    image_data['image_url'] = temp_property['thumb2']
    image_data['property_id'] = temp_property['ref_id']
    image_data['image_type'] = random.choice(['indoor', 'outdoor'])
    image_csv_data.append(image_data)

    agend_data = {}
    agend_data['property_id'] = temp_property['ref_id']
    agend_data['agent_name'] = ''
    agend_data['primary_phone'] = temp_property['phone']
    agend_data['primary_email'] = str(temp_property['phone'])+'@gmail.com'
    agent_csv_data.append(agend_data)


parent_path = './real_data/'

propert_csv_df = pd.DataFrame.from_records(propert_csv_data)
propert_csv_df.to_csv(file_name+'_property.csv')

image_csv_df = pd.DataFrame.from_records(image_csv_data)
image_csv_df.to_csv(file_name+'_image.csv')

agent_csv_df = pd.DataFrame.from_records(agent_csv_data)
agent_csv_df.to_csv(file_name+'_agent.csv')