import sqlite3 as sq
import pandas as pd


class sql_db():
    def __init__(self):
        # connect SQL server
        # conn = sq.connect('mysql.db')
        self.conn = sq.connect(":memory:?cache=shared")
        self.c = self.conn.cursor()  
        self.c.executescript('''
            drop table if exists property_table;
            CREATE TABLE property_table (
                property_id int NOT NULL PRIMARY KEY,
                property_name VARCHAR(255),
                description VARCHAR(255),
                num_bedroom INT,
                num_bathroom Float,
                area_size INT,
                price FLOAT(10,2),
                transaction_type TEXT CHECK( transaction_type IN ('Buy', 'Rent') ),
                property_types TEXT CHECK( property_types IN ('Condo', 'Apartment', 'House', 'Townhouse') ),
                parking TEXT CHECK( parking IN ('garage', 'underground', 'covered', 'outdoor') ),
                laundry TEXT CHECK( laundry IN ('in_suite', 'shared') ),
                furnished BOOL,
                pet_friendly BOOL,
                longtidude decimal(10,7),
                latitude decimal(10,7),
                build_year YEAR,
                air_conditioning Bool,
                hardwood_floors Bool,
                balcony Bool
            );
            CREATE TABLE image_table (
                image_id int not null,
                property_id int not null,
                image_type TEXT CHECK( image_type IN ('indoor', 'outdoor') ),
                image_url text,
                PRIMARY KEY (image_id),
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            );
            CREATE TABLE agent_table (
                agend_id int not null,
                property_id int not null,
                primary_email text,
                primary_phone text,
                PRIMARY KEY (agend_id),
                FOREIGN KEY (property_id) REFERENCES property_table(property_id)
            )
        ''')
        self.conn.commit()

    def convert_csv_to_sql(self, table_name='property_table', csv_file_name='property_table.csv'):
        sql_script = ""
        if table_name == 'property_table':
            df = pd.read_csv(csv_file_name)
            print (df.columns.tolist())
            for row in df.itertuples():
                sql_script = '''
                    INSERT INTO property_table (property_id, property_name, description, num_bedroom, num_bathroom, 
                    area_size, price, transaction_type, property_types, parking, laundry, furnished, pet_friendly,
                    longtidude, latitude, build_year, air_conditioning, hardwood_floors, balcony)
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
                self.c.execute(sql_script, record)
            self.conn.commit()
        else:
            pass
        return 

    def get_list_properties(self, sql_command="SELECT * FROM property_table;"):
        self.c .execute(sql_command) 
        data = self.c.fetchall()
        return data

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    sql_class = sql_db()
    sql_class.convert_csv_to_sql( table_name='property_table', csv_file_name='../database/property_table.csv')
    data = sql_class.get_list_properties()
    print (data)
    sql_class.close()
