import sqlite3 as sq

class sql_db():
    def __init__(self):
        # connect SQL server
        # conn = sq.connect('mysql.db')
        self.conn = sq.connect("file::memory:?cache=shared")
        self.c = self.conn.cursor()  
        self.c.executescript('''
            drop table if exists property_table;
            CREATE TABLE property_table (
                property_id int NOT NULL PRIMARY KEY,
                property_name VARCHAR(255),
                description VARCHAR(255),
                num_bedroom INT,
                num_bathroom INT,
                area_size INT,
                price FLOAT(10,2),
                transaction_type TEXT CHECK( property_type IN ('Buy', 'Rent') ),
                property_types TEXT CHECK( property_types IN ('Condo', 'Apartment', 'House') ),
                parking TEXT CHECK( parking IN ('garage', 'underground', 'covered', 'outdoor') ),
                laundry TEXT CHECK( laundry IN ('in_suite', 'shared') ),
                furnished BOOL,
                pet_friendly BOOL,
                longtidude decimal(10,7),
                latitude decimal(10,7),
                build_year YEAR,
                smoking_allowed Bool,
                air_conditioning Bool,
                hardwood_floors Bool,
                balcony Bool
            );
        ''')
        self.conn.commit()

    def close(self):
        self.conn.close()




if __name__ == "__main__":
    sql_class = sql_db()
    sql_class.close()