import os
import sqlite3
from typing import List, Optional, Tuple, Any
import pandas as pd

current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(current_file_directory, 'property_database')
class Database:
    def __init__(self, database_name = database_path):
        self.database_name = database_name
        self._create_table()

    def get_connection(self):
        conn = sqlite3.connect(self.database_name, uri=True)
        cursor = conn.cursor()
        return conn, cursor

    def _create_table(self):
        query = ''
        query += self.get_property_table_definition()
        query += self.get_image_table_definition()
        query += self.get_agent_table_definition()
        
        conn, cursor = self.get_connection()
        cursor.executescript('DROP TABLE if exists property_table;DROP TABLE if exists image_table;DROP TABLE if exists agent_table;'+query)
        # cursor.execute(query)
        conn.commit()
        conn.close()

    def get_property_table_definition(self) -> str:
        return '''  CREATE TABLE property_table (
                    property_id int NOT NULL PRIMARY KEY,
                    property_name VARCHAR(255),
                    description VARCHAR(255),
                    num_bedroom INT,
                    num_bathroom INT,
                    area_size INT,
                    price FLOAT,
                    transaction_type TEXT CHECK( transaction_type IN ('Buy', 'Rent') ),
                    property_type TEXT CHECK( property_type IN ('Condo', 'Apartment', 'House', 'Townhouse') ),
                    parking TEXT CHECK( parking IN ('garage', 'underground', 'covered', 'outdoor') ),
                    laundry TEXT CHECK( laundry IN ('in_suite', 'shared') ),
                    furnished BOOL,
                    pet_friendly BOOL,
                    longitude DECIMAL(10,7),
                    latitude DECIMAL(10,7),
                    build_year YEAR,
                    smoking_allowed BOOL,
                    air_conditioning BOOL,
                    hardwood_floors BOOL,
                    balcony BOOL
                );'''

    def get_image_table_definition(self) -> str:
        return '''CREATE TABLE image_table (
                image_id int not null,
                property_id int not null,
                image_type TEXT CHECK( image_type IN ('indoor', 'outdoor') ),
                image_url text,
                PRIMARY KEY (image_id),
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            );'''

    def get_agent_table_definition(self) -> str:
        return '''CREATE TABLE agent_table (
                agend_id int not null,
                property_id int not null,
                primary_email text,
                primary_phone text,
                PRIMARY KEY (agend_id),
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            );'''

    def convert_csv_to_sql(self, table_name='property_table', csv_file_name='property_table.csv'):
        conn, cursor = self.get_connection()
        sql_script = ""
        if table_name == 'property_table':
            df = pd.read_csv(csv_file_name)
            print (df.columns.tolist())
            for row in df.itertuples():
                sql_script = '''
                    INSERT INTO property_table (property_id, property_name, description, num_bedroom, num_bathroom, 
                    area_size, price, transaction_type, property_type, parking, laundry, furnished, pet_friendly,
                    longitude, latitude, build_year, air_conditioning, hardwood_floors, balcony)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    '''
                    #
                record = (row.property_id, 
                    row.property_name,
                    row.description,
                    row.num_bedroom,
                    row.num_bathroom,
                    row.area_size,
                    row.price,
                    row.transaction_type,
                    row.property_types,
                    row.parking,
                    row.laundry,
                    row.furnished,                    
                    row.pet_friendly,
                    row.longitude,
                    row.latitude,
                    row.build_year,
                    row.air_conditioning,
                    row.hardwood_floors,
                    row.balcony)
                cursor.execute(sql_script, record)
            conn.commit()
            conn.close()
        else:
            pass
        return 

    def insert_row(self, table_name: str, data: List[List[Any]]):
        conn, cursor = self.get_connection()
        print(data)
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

    def execute_query(self, query: str, params: Optional[Tuple] = None):
        conn, cursor = self.get_connection()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_query(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        conn, cursor = self.get_connection()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result


if __name__ == "__main__":
    sql_class = Database()
    sql_class.convert_csv_to_sql( table_name='property_table', csv_file_name='../database/property_table.csv')
    data = sql_class.fetch_query(query='SELECT * FROM property_table;')
    print (data)
    # sql_class.close()