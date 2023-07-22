CREATE DATABASE IF NOT EXISTS `homefinder`;
USE homefinder;
CREATE TABLE property_table (
    propertyId int NOT NULL PRIMARY KEY,
    property_name VARCHAR(255),
    description VARCHAR(255),
    num_bedroom INT,
    num_bathroom INT,
    area_size INT,
    price FLOAT(10,2),
    property_type ENUM("Buy", "Rent"),
    furnished BOOL,
    pet_friendly BOOL,
    longtidude decimal(10,7),
    latitude decimal(10,7),
    property_types ENUM("Condo", "Apartment", "House"),
    build_year YEAR,
    smoking_allowed Bool,
    parking ENUM("garage", "underground", "covered", "outdoor"),
    laundry ENUM("in_suite", "shared"),
    air_conditioning Bool,
    hardwood_floors Bool,
    balcony Bool
);
