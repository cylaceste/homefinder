import sqlite3 as sq

def sql_init():
    # connect SQL server
    conn = sq.connect('mysql.db')
    # conn = sq.connect("file::memory:?cache=shared")

    c = conn.cursor()    
    c.executescript('''
    drop table if exists property_table;
    CREATE TABLE property_table (
        propertyId int NOT NULL PRIMARY KEY,
        property_name VARCHAR(255),
        description VARCHAR(255),
        num_bedroom INT,
        num_bathroom INT,
        area_size INT,
        price FLOAT(10,2),
        property_type TEXT CHECK( property_type IN ('Buy', 'Rent') ),
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
    conn.commit()
    conn.close()
    return



if __name__ == "__main__":
    sql_init()