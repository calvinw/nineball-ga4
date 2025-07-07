#!/usr/bin/env python3
"""
Test direct GA4 API access to verify permissions
"""

import json
import airbyte as ab
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
GA4_PROPERTY_ID = "495652498"
CREDENTIALS_FILE = "ga4-data-extraction-465113-63dae243465a.json"

def test_ga4_permissions():
    """Test if service account has access to GA4 property"""
    try:
        credentials = json.load(open(CREDENTIALS_FILE))
        
        # Create a very simple custom report to test access
        print("Testing GA4 access with minimal report...")
        
        source = ab.get_source(
            "source-google-analytics-data-api",
            config={
                "property_ids": [GA4_PROPERTY_ID],
                "credentials": {
                    "credentials_json": json.dumps(credentials)
                },
                "date_ranges": [
                    {
                        "start_date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                        "end_date": datetime.now().strftime("%Y-%m-%d")
                    }
                ],
                "custom_reports": [
                    {
                        "name": "basic_test",
                        "dimensions": ["date"],
                        "metrics": ["sessions"]
                    }
                ]
            },
            install_if_missing=True
        )
        
        print("✓ Source created, checking connection...")
        
        # Test connection
        check_result = source.check()
        print(f"Check result: {check_result}")
        
        # Try to discover streams
        streams = source.get_available_streams()
        print(f"Available streams: {streams}")
        
        if streams:
            print("✓ Connection successful!")
            return True
        else:
            print("✗ No streams available")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_property_id():
    """Test if the property ID is correctly formatted"""
    print(f"Testing property ID: {GA4_PROPERTY_ID}")
    
    if not GA4_PROPERTY_ID.isdigit():
        print("✗ Property ID should be numeric")
        return False
        
    if len(GA4_PROPERTY_ID) < 9:
        print("✗ Property ID seems too short")
        return False
        
    print("✓ Property ID format looks correct")
    return True

def main():
    print("Testing GA4 direct access...")
    
    # Test property ID format
    if not test_property_id():
        return 1
    
    # Test GA4 permissions
    if not test_ga4_permissions():
        return 1
    
    print("\n✓ GA4 access test completed!")
    return 0

if __name__ == "__main__":
    exit(main())