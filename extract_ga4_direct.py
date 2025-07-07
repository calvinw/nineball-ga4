#!/usr/bin/env python3
"""
GA4 Data Extraction using Google Analytics Data API directly
Extracts GA4 data and exports to CSV files for Dolt upload
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GA4_PROPERTY_ID = "495652498"
CREDENTIALS_FILE = "ga4-data-extraction-465113-63dae243465a.json"
DAYS_BACK = 30

def get_analytics_client():
    """Initialize GA4 client with service account credentials"""
    credentials_path = Path(CREDENTIALS_FILE)
    if not credentials_path.exists():
        raise FileNotFoundError(f"Service account file not found: {CREDENTIALS_FILE}")
    
    credentials = service_account.Credentials.from_service_account_file(
        str(credentials_path)
    )
    
    # Add the required scope
    credentials = credentials.with_scopes(['https://www.googleapis.com/auth/analytics.readonly'])
    
    client = BetaAnalyticsDataClient(credentials=credentials)
    return client

def run_report(client, dimensions, metrics, date_range_start, date_range_end):
    """Run a GA4 report with specified dimensions and metrics"""
    property_id = f"properties/{GA4_PROPERTY_ID}"
    
    request = RunReportRequest(
        property=property_id,
        dimensions=[Dimension(name=dim) for dim in dimensions],
        metrics=[Metric(name=metric) for metric in metrics],
        date_ranges=[DateRange(start_date=date_range_start, end_date=date_range_end)],
    )
    
    response = client.run_report(request=request)
    return response

def response_to_dataframe(response, dimensions, metrics):
    """Convert GA4 response to pandas DataFrame"""
    data = []
    
    for row in response.rows:
        row_data = {}
        
        # Add dimensions
        for i, dim in enumerate(dimensions):
            row_data[dim] = row.dimension_values[i].value
        
        # Add metrics
        for i, metric in enumerate(metrics):
            value = row.metric_values[i].value
            # Convert to appropriate type
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except:
                pass  # Keep as string if conversion fails
            row_data[metric] = value
        
        data.append(row_data)
    
    return pd.DataFrame(data)

def extract_sessions_data(client, start_date, end_date):
    """Extract sessions data"""
    print("Extracting sessions data...")
    
    dimensions = [
        "date",
        "sessionSource", 
        "sessionMedium",
        "country",
        "deviceCategory"
    ]
    
    metrics = [
        "sessions",
        "activeUsers",
        "averageSessionDuration",
        "bounceRate"
    ]
    
    try:
        response = run_report(client, dimensions, metrics, start_date, end_date)
        df = response_to_dataframe(response, dimensions, metrics)
        
        # Clean column names
        df.columns = [col.lower().replace('session', '').replace('source', 'source').replace('medium', 'medium') for col in df.columns]
        
        return df
    except Exception as e:
        print(f"Error extracting sessions data: {e}")
        return pd.DataFrame()

def extract_pages_data(client, start_date, end_date):
    """Extract pages data"""
    print("Extracting pages data...")
    
    dimensions = [
        "date",
        "pagePath",
        "pageTitle",
        "sessionSource",
        "sessionMedium"
    ]
    
    metrics = [
        "screenPageViews",
        "userEngagementDuration"
    ]
    
    try:
        response = run_report(client, dimensions, metrics, start_date, end_date)
        df = response_to_dataframe(response, dimensions, metrics)
        
        # Clean column names and rename for consistency
        df.columns = [col.lower().replace('screen', '').replace('session', '') for col in df.columns]
        df.rename(columns={
            'pageviews': 'page_views',
            'userengagementduration': 'avg_time_on_page'
        }, inplace=True)
        
        return df
    except Exception as e:
        print(f"Error extracting pages data: {e}")
        return pd.DataFrame()

def extract_events_data(client, start_date, end_date):
    """Extract events data"""
    print("Extracting events data...")
    
    dimensions = [
        "date",
        "eventName",
        "sessionSource",
        "sessionMedium"
    ]
    
    metrics = [
        "eventCount",
        "eventValue"
    ]
    
    try:
        response = run_report(client, dimensions, metrics, start_date, end_date)
        df = response_to_dataframe(response, dimensions, metrics)
        
        # Clean column names
        df.columns = [col.lower().replace('session', '') for col in df.columns]
        
        return df
    except Exception as e:
        print(f"Error extracting events data: {e}")
        return pd.DataFrame()

def extract_conversions_data(client, start_date, end_date):
    """Extract conversions data"""
    print("Extracting conversions data...")
    
    dimensions = [
        "date",
        "eventName",
        "sessionSource", 
        "sessionMedium"
    ]
    
    metrics = [
        "conversions",
        "totalRevenue"
    ]
    
    try:
        response = run_report(client, dimensions, metrics, start_date, end_date)
        df = response_to_dataframe(response, dimensions, metrics)
        
        # Clean column names and filter for conversion events
        df.columns = [col.lower().replace('session', '') for col in df.columns]
        df.rename(columns={
            'eventname': 'conversion_name',
            'totalrevenue': 'conversion_value'
        }, inplace=True)
        
        # Only keep rows where conversions > 0
        df = df[df['conversions'] > 0]
        
        return df
    except Exception as e:
        print(f"Error extracting conversions data: {e}")
        return pd.DataFrame()

def export_to_csv(dataframes):
    """Export DataFrames to CSV files"""
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    csv_files = {
        "sessions_data": "sessions_data.csv",
        "pages_data": "pages_data.csv",
        "events_data": "events_data.csv", 
        "conversions_data": "conversions_data.csv"
    }
    
    for data_name, csv_filename in csv_files.items():
        if data_name in dataframes and not dataframes[data_name].empty:
            csv_path = data_dir / csv_filename
            dataframes[data_name].to_csv(csv_path, index=False)
            print(f"✓ Exported {len(dataframes[data_name])} rows to {csv_path}")
            
            # Show sample data
            print(f"Sample data from {data_name}:")
            print(dataframes[data_name].head(2))
            print()
        else:
            print(f"⚠ No data found for {data_name}")

def main():
    """Main extraction function"""
    try:
        print("Starting GA4 data extraction using Google Analytics Data API...")
        print(f"Property ID: {GA4_PROPERTY_ID}")
        print(f"Date range: Last {DAYS_BACK} days")
        
        # Initialize client
        client = get_analytics_client()
        print("✓ GA4 client initialized")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=DAYS_BACK)
        
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        print(f"Date range: {start_date_str} to {end_date_str}")
        
        # Extract data
        dataframes = {}
        
        dataframes["sessions_data"] = extract_sessions_data(client, start_date_str, end_date_str)
        dataframes["pages_data"] = extract_pages_data(client, start_date_str, end_date_str)
        dataframes["events_data"] = extract_events_data(client, start_date_str, end_date_str)
        dataframes["conversions_data"] = extract_conversions_data(client, start_date_str, end_date_str)
        
        # Export to CSV
        export_to_csv(dataframes)
        
        print("\n✓ GA4 data extraction completed successfully!")
        print("CSV files are ready in the 'data/' directory for Dolt upload.")
        
    except Exception as e:
        print(f"✗ Error during extraction: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())