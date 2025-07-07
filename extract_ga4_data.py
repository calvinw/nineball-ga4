#!/usr/bin/env python3
"""
GA4 Data Extraction Script using PyAirbyte
Extracts GA4 data and exports to CSV files for Dolt upload
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import airbyte as ab
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GA4_PROPERTY_ID = "495652498"
CREDENTIALS_FILE = "ga4-data-extraction-465113-63dae243465a.json"
DAYS_BACK = 30

def load_service_account_credentials():
    """Load service account credentials from JSON file"""
    credentials_path = Path(CREDENTIALS_FILE)
    if not credentials_path.exists():
        raise FileNotFoundError(f"Service account file not found: {CREDENTIALS_FILE}")
    
    with open(credentials_path, 'r') as f:
        credentials = json.load(f)
    
    return credentials

def setup_ga4_source():
    """Configure GA4 source with PyAirbyte"""
    credentials = load_service_account_credentials()
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_BACK)
    
    # GA4 source configuration with custom reports
    source = ab.get_source(
        "source-google-analytics-data-api",
        config={
            "property_ids": [GA4_PROPERTY_ID],
            "credentials": {
                "credentials_json": json.dumps(credentials)
            },
            "date_ranges": [
                {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
            ],
            "custom_reports": [
                {
                    "name": "sessions_report",
                    "dimensions": [
                        "date",
                        "sessionSource",
                        "sessionMedium",
                        "country",
                        "deviceCategory"
                    ],
                    "metrics": [
                        "sessions",
                        "activeUsers",
                        "averageSessionDuration",
                        "bounceRate"
                    ]
                },
                {
                    "name": "pages_report",
                    "dimensions": [
                        "date",
                        "pagePath",
                        "pageTitle",
                        "sessionSource",
                        "sessionMedium"
                    ],
                    "metrics": [
                        "screenPageViews"
                    ]
                },
                {
                    "name": "events_report",
                    "dimensions": [
                        "date",
                        "eventName",
                        "sessionSource",
                        "sessionMedium"
                    ],
                    "metrics": [
                        "eventCount"
                    ]
                }
            ]
        }
    )
    
    return source

def extract_data():
    """Extract GA4 data using PyAirbyte"""
    print("Setting up GA4 source...")
    source = setup_ga4_source()
    
    print("Checking source configuration...")
    source.check()
    
    print("Extracting data...")
    # Use DuckDB as local cache
    cache = ab.get_default_cache()
    
    # Extract data
    result = source.read(cache=cache)
    
    return result, cache

def export_to_csv(cache):
    """Export data from DuckDB cache to CSV files"""
    print("Exporting data to CSV files...")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # First, let's see what tables are available
    print("Available tables in cache:")
    try:
        tables = cache.get_table_names()
        for table in tables:
            print(f"  - {table}")
    except Exception as e:
        print(f"Error getting table names: {e}")
        return
    
    # Export all available tables
    for table_name in tables:
        try:
            # Query data from DuckDB cache
            df = cache.get_pandas_df(table_name)
            
            if not df.empty:
                # Clean column names for CSV
                df.columns = [col.lower().replace(' ', '_') for col in df.columns]
                
                # Export to CSV
                csv_path = data_dir / f"{table_name}.csv"
                df.to_csv(csv_path, index=False)
                print(f"✓ Exported {len(df)} rows to {csv_path}")
                
                # Show first few rows as sample
                print(f"Sample data from {table_name}:")
                print(df.head(2))
                print()
            else:
                print(f"⚠ No data found for {table_name}")
                
        except Exception as e:
            print(f"✗ Error exporting {table_name}: {e}")

def main():
    """Main extraction function"""
    try:
        print("Starting GA4 data extraction...")
        print(f"Property ID: {GA4_PROPERTY_ID}")
        print(f"Date range: Last {DAYS_BACK} days")
        
        # Extract data
        result, cache = extract_data()
        
        # Export to CSV
        export_to_csv(cache)
        
        print("\n✓ GA4 data extraction completed successfully!")
        print("CSV files are ready in the 'data/' directory for Dolt upload.")
        
    except Exception as e:
        print(f"✗ Error during extraction: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())