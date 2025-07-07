-- GA4 Data Tables for Dolt (Corrected to match CSV columns)
-- Run with: dolt sql < create_ga4_tables_corrected.sql

-- Drop existing tables
DROP TABLE IF EXISTS sessions_data;
DROP TABLE IF EXISTS pages_data;
DROP TABLE IF EXISTS events_data;
DROP TABLE IF EXISTS conversions_data;

-- Sessions data table (matching actual CSV columns)
CREATE TABLE sessions_data (
    date DATE,
    source VARCHAR(255),
    medium VARCHAR(255),
    country VARCHAR(100),
    devicecategory VARCHAR(50),
    s INT,  -- sessions column got renamed to 's'
    activeusers INT,
    averageduration FLOAT,
    bouncerate FLOAT,
    PRIMARY KEY (date, source, medium, country, devicecategory)
);

-- Pages data table (matching actual CSV columns)
CREATE TABLE pages_data (
    date DATE,
    pagepath VARCHAR(500),
    pagetitle VARCHAR(500),
    source VARCHAR(255),
    medium VARCHAR(255),
    page_views INT,
    avg_time_on_page FLOAT,
    PRIMARY KEY (date, pagepath, source, medium)
);

-- Events data table (matching actual CSV columns)
CREATE TABLE events_data (
    date DATE,
    eventname VARCHAR(255),
    source VARCHAR(255),
    medium VARCHAR(255),
    eventcount INT,
    eventvalue FLOAT,
    PRIMARY KEY (date, eventname, source, medium)
);

-- Conversions data table (matching actual CSV columns)
CREATE TABLE conversions_data (
    date DATE,
    conversion_name VARCHAR(255),
    source VARCHAR(255),
    medium VARCHAR(255),
    conversions INT,
    conversion_value FLOAT,
    PRIMARY KEY (date, conversion_name, source, medium)
);

-- Show created tables
SHOW TABLES;