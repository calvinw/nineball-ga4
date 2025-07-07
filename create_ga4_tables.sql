-- GA4 Data Tables for Dolt
-- Run with: dolt sql < create_ga4_tables.sql

-- Sessions data table
CREATE TABLE IF NOT EXISTS sessions_data (
    date DATE,
    source VARCHAR(255),
    medium VARCHAR(255),
    country VARCHAR(100),
    device_category VARCHAR(50),
    sessions INT,
    active_users INT,
    avg_session_duration FLOAT,
    bounce_rate FLOAT,
    PRIMARY KEY (date, source, medium, country, device_category)
);

-- Pages data table
CREATE TABLE IF NOT EXISTS pages_data (
    date DATE,
    page_path VARCHAR(500),
    page_title VARCHAR(500),
    source VARCHAR(255),
    medium VARCHAR(255),
    page_views INT,
    unique_page_views INT,
    avg_time_on_page FLOAT,
    PRIMARY KEY (date, page_path, source, medium)
);

-- Events data table
CREATE TABLE IF NOT EXISTS events_data (
    date DATE,
    event_name VARCHAR(255),
    source VARCHAR(255),
    medium VARCHAR(255),
    page_path VARCHAR(500),
    event_count INT,
    event_value FLOAT,
    PRIMARY KEY (date, event_name, source, medium, page_path)
);

-- Conversions data table
CREATE TABLE IF NOT EXISTS conversions_data (
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