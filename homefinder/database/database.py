import os
import sqlite3
from typing import List, Optional, Tuple, Any
current_file_directory = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(current_file_directory, 'property_database')
class PropertyDatabase:
    def __init__(self, database_name = database_path):
        self.database_name = database_name
        self._create_property_table()

    def get_connection(self):
        conn = sqlite3.connect(self.database_name, uri=True)
        cursor = conn.cursor()
        return conn, cursor

    def _create_property_table(self):
        query = self.get_property_table_definition()
        conn, cursor = self.get_connection()
        cursor.execute('DROP TABLE if exists property_table ')
        cursor.execute(query)
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
                    property_type TEXT CHECK( property_type IN ('Condo', 'Apartment', 'House') ),
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
        field_names = [i[0] for i in cursor.description]
        conn.close()
        return result, field_names
