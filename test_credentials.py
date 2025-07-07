#!/usr/bin/env python3
"""
Test GA4 credentials and PyAirbyte source configuration
"""

import json
import airbyte as ab
from pathlib import Path

# Configuration
GA4_PROPERTY_ID = "495652498"
CREDENTIALS_FILE = "ga4-data-extraction-465113-63dae243465a.json"

def test_credentials():
    """Test if credentials file exists and is valid JSON"""
    credentials_path = Path(CREDENTIALS_FILE)
    
    if not credentials_path.exists():
        print(f"✗ Credentials file not found: {CREDENTIALS_FILE}")
        return False
    
    try:
        with open(credentials_path, 'r') as f:
            credentials = json.load(f)
        
        print(f"✓ Credentials file loaded successfully")
        print(f"  - Project ID: {credentials.get('project_id', 'Not found')}")
        print(f"  - Client Email: {credentials.get('client_email', 'Not found')}")
        print(f"  - Type: {credentials.get('type', 'Not found')}")
        return True
        
    except Exception as e:
        print(f"✗ Error loading credentials: {e}")
        return False

def test_source_discovery():
    """Test PyAirbyte source discovery"""
    try:
        # Try to discover what sources are available
        print("\nTesting PyAirbyte source discovery...")
        
        # Check if source exists
        source_name = "source-google-analytics-data-api"
        print(f"Attempting to get source: {source_name}")
        
        # Try minimal config first
        source = ab.get_source(
            source_name,
            config={
                "property_ids": [GA4_PROPERTY_ID],
                "credentials": {
                    "credentials_json": json.dumps(json.load(open(CREDENTIALS_FILE)))
                }
            },
            install_if_missing=True
        )
        
        print(f"✓ Source created successfully")
        
        # Try to discover schema
        print("Discovering schema...")
        try:
            catalog = source.get_available_streams()
            print(f"✓ Found {len(catalog)} available streams:")
            for stream in catalog:
                print(f"  - {stream}")
        except Exception as e:
            print(f"✗ Schema discovery failed: {e}")
            
        return True
        
    except Exception as e:
        print(f"✗ Source creation failed: {e}")
        return False

def main():
    print("Testing GA4 credentials and PyAirbyte configuration...")
    
    # Test credentials
    if not test_credentials():
        return 1
    
    # Test source
    if not test_source_discovery():
        return 1
    
    print("\n✓ All tests passed!")
    return 0

if __name__ == "__main__":
    exit(main())