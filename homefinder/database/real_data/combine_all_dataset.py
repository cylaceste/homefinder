import pandas as pd

file_list = ['rent_1', 'sale_1', 'sale_2', 'sale_3', 'sale_4', 'sale_5',
'sale_6', 'sale_7', 'sale_8', 'sale_9', 'sale_10']
target_path = '../'
property_table_files = []
image_table_files = []
agent_table_files = []
for file in file_list:

    property_table_files.append(pd.read_csv(file+'_property.csv'))
    image_table_files.append(pd.read_csv(file+'_image.csv'))
    agent_table_files.append(pd.read_csv(file+'_agent.csv'))
    
print ()
property_df = pd.concat(property_table_files)
property_df.to_csv(target_path+'property_table.csv')
pd.concat(image_table_files).to_csv(target_path+'image_table.csv')
pd.concat(agent_table_files).to_csv(target_path+'agent_table.csv')
