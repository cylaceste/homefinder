import os
import sqlite3
from typing import List, Optional, Tuple, Any
import pandas as pd

current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(current_file_directory, 'property_database')
property_table_csv = os.path.join(current_file_directory, 'property_table.csv')
image_table_csv = os.path.join(current_file_directory, 'image_table.csv')
agent_table_csv = os.path.join(current_file_directory, 'agent_table.csv')

class Database:
    def __init__(self, database_name = database_path):
        self.database_name = database_name
        self._create_table()
        self._convert_csv_to_sql( table_name='property_table', csv_file_name=property_table_csv)
        self._convert_csv_to_sql( table_name='image_table', csv_file_name=image_table_csv)
        self._convert_csv_to_sql( table_name='agent_table', csv_file_name=agent_table_csv)

    def _get_connection(self):
        conn = sqlite3.connect(self.database_name, uri=True)
        return conn, conn.cursor()

    def _create_table(self):
        query = ''
        query += self._get_property_table_definition()
        query += self._get_image_table_definition()
        query += self._get_agent_table_definition()
        
        conn, cursor = self._get_connection()
        cursor.executescript('DROP TABLE if exists property_table;DROP TABLE if exists image_table;DROP TABLE if exists agent_table;'+query)
        # cursor.execute(query)
        conn.commit()
        conn.close()

    def _get_property_table_definition(self) -> str:
        return '''  CREATE TABLE property_table (
                    property_id int NOT NULL PRIMARY KEY,
                    property_name VARCHAR(255),
                    address Text,
                    description VARCHAR(255),
                    num_bedroom INT,
                    num_bathroom INT,
                    area_size INT,
                    price FLOAT,
                    transaction_type TEXT CHECK( transaction_type IN ('Buy', 'Rent') ),
                    property_type TEXT CHECK( property_type IN ('Apartment', 'Townhouse', 'Condo Unit', 'House', 'Duplex', 'Basement',
 'Main Floor', 'Room For Rent', 'Loft', 'Office Space') ),
                    parking TEXT CHECK( parking IN ('garage', 'underground', 'covered', 'outdoor', 'no') ),
                    laundry TEXT CHECK( laundry IN ('in_suite', 'shared') ),
                    furnished BOOL,
                    pet_friendly BOOL,
                    latitude DECIMAL(10,7),
                    longitude DECIMAL(10,7),
                    build_year YEAR,
                    smoking_allowed BOOL,
                    air_conditioning BOOL,
                    hardwood_floors BOOL,
                    balcony BOOL
                );'''

    def _get_image_table_definition(self) -> str:
        return '''CREATE TABLE image_table (
                image_id int not null,
                property_id int not null,
                image_type TEXT CHECK( image_type IN ('indoor', 'outdoor') ),
                image_url text,
                PRIMARY KEY (image_id),
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            );
            CREATE INDEX idx_property_id ON image_table (property_id);
            '''

    def _get_agent_table_definition(self) -> str:
        return '''CREATE TABLE agent_table (
                property_id int not null,
                primary_email text,
                primary_phone text,
                agent_name text,
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            );'''

    def _convert_csv_to_sql(self, table_name='property_table', csv_file_name='property_table.csv'):
        conn, cursor = self._get_connection()
        sql_script = ""
        if table_name == 'property_table':
            df = pd.read_csv(csv_file_name)
            for row in df.itertuples():
                sql_script = '''
                    INSERT INTO property_table (property_id, property_name, description, num_bedroom, num_bathroom, 
                    area_size, price, transaction_type, property_type, parking, laundry, furnished, pet_friendly,
                    latitude, longitude, build_year, air_conditioning, hardwood_floors, balcony)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                record = (row.property_id, 
                    row.property_name,
                    row.description,
                    row.num_bedroom,
                    row.num_bathroom,
                    row.area_size,
                    row.price,
                    row.transaction_type,
                    row.property_type,
                    row.parking,
                    row.laundry,
                    row.furnished,                    
                    row.pet_friendly,
                    row.latitude,
                    row.longitude,
                    row.build_year,
                    row.air_conditioning,
                    row.hardwood_floors,
                    row.balcony)
                cursor.execute(sql_script, record)
            conn.commit()
            conn.close()
        elif table_name == 'image_table':
            df = pd.read_csv(csv_file_name)
            for row in df.itertuples():
                sql_script = '''
                    INSERT INTO image_table (image_id, property_id, image_type, image_url)
                    VALUES (?, ?, ?, ?)
                    '''
                record = (row.image_id, row.property_id, row.image_type, row.image_url)
                cursor.execute(sql_script, record)
            conn.commit()
            conn.close()
        elif table_name == 'agent_table':
            df = pd.read_csv(csv_file_name)
            for row in df.itertuples():
                sql_script = '''
                    INSERT INTO agent_table (property_id, primary_email, primary_phone)
                    VALUES (?, ?, ?)
                    '''
                record = (row.property_id, row.primary_email, row.primary_phone)
                cursor.execute(sql_script, record)
            conn.commit()
            conn.close()
        else:
            pass
        return 

    def insert_row(self, table_name: str, data: List[List[Any]]):
        conn, cursor = self._get_connection()
        if isinstance(data[0], list):
            placeholders = ', '.join('?' * len(data[0]))
            query = f'INSERT INTO {table_name} VALUES ({placeholders})'
            cursor.executemany(query, data)
        else:
            placeholders = ', '.join('?' * len(data))
            query = f'INSERT INTO {table_name} VALUES ({placeholders})'
            cursor.execute(query, data)
        conn.commit()
        conn.close()

    def _execute_query(self, query: str, params: Optional[Tuple] = None):
        conn, cursor = self._get_connection()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_query(self, query: str, params: Optional[Tuple] = None) -> Tuple[List[Tuple[Any]], List[str]]:
        conn, cursor = self._get_connection()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        result = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        conn.close()
        return result, field_names
    
    def get_database_definition(self) -> str:
        return ';\n'.join(table_defn[0] for table_defn in self.fetch_query(query='SELECT sql FROM sqlite_master;')[0] if table_defn[0])

if __name__ == "__main__":
    sql_class = Database()
    query='SELECT sql FROM sqlite_master;'
    query='''
    SELECT property_table.property_id, property_table.description AS property_description, property_table.latitude, property_table.longitude, 
       property_table.num_bedroom, GROUP_CONCAT(image_table.image_url) AS image_urls
FROM property_table
LEFT JOIN image_table ON property_table.property_id = image_table.property_id
WHERE property_table.num_bedroom >= 3 AND property_table.latitude BETWEEN 53.3 AND 53.7 AND property_table.longitude BETWEEN -113.7 AND -113.3
GROUP BY property_table.property_id
LIMIT 10;
'''
    query = "SELECT LIMIT 10 property_name, description, num_bedroom, num_bathroom, area_size, price, transaction_type, property_type, parking, laundry, furnished, pet_friendly, latitude, longitude, build_year, smoking_allowed, air_conditioning, hardwood_floors, balcony, GROUP_CONCAT(image_url) as image_urls FROM property_table INNER JOIN image_table ON property_table.property_id = image_table.property_id WHERE num_bedroom >= 5 AND property_type = 'House' GROUP BY property_table.property_id"
    data = sql_class.fetch_query(query=query)[0]
    print(data)
    # print(sql_class.get_database_definition())
    # sql_class.close()
