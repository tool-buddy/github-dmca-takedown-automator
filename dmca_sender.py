#!/usr/bin/env python3
"""
DMCA Takedown Request Sender

This script processes DMCA takedown request configuration files and sends
emails to GitHub based on the configuration. Each config file should contain
all necessary information for a single DMCA request.

Usage:
    python dmca_sender.py request1.json [request2.json ...]
"""

import argparse
import json
import os
import sys
from utils.email_utils import preview_email, send_email, get_user_confirmation


def load_config(config_path):
    """
    Load a config file and validate its contents.
    
    Args:
        config_path (str): Path to the config file.
        
    Returns:
        dict: The loaded configuration data.
        
    Raises:
        ValueError: If the config file is missing required fields.
    """
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Check for required fields (all fields are now required)
        required_fields = [
            'from', 'copyright_holder_or_authorized', 
            'is_revised', 'content_source', 'ownership', 'work_description',
            'infringing_urls', 'access_control', 'forks_information',
            'open_source', 'solution', 'contact', 'legal_name',
            'contact_email', 'phone'
        ]
        
        missing_fields = [field for field in required_fields if not config_data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Config file missing required fields: {', '.join(missing_fields)}")
            
        # Validate URLs
        if not isinstance(config_data.get('infringing_urls', []), list):
            raise ValueError("'infringing_urls' must be a list")
        
        if not config_data.get('infringing_urls'):
            raise ValueError("'infringing_urls' cannot be empty")
            
        return config_data
        
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in config file: {config_path}")
    except FileNotFoundError:
        raise ValueError(f"Config file not found: {config_path}")


def process_config(config_path):
    """
    Process a single config file.
    
    Args:
        config_path (str): Path to the config file.
        
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        # Load and validate the config
        print(f"\nProcessing config file: {config_path}")
        config_data = load_config(config_path)
        
        # Preview the email
        preview = preview_email(config_data)
        print(preview)
        
        # Get user confirmation
        if get_user_confirmation():
            # Send the email
            return send_email(config_data)
        else:
            print("Email sending cancelled by user.")
            return False
            
    except ValueError as e:
        print(f"Error processing config file: {e}", file=sys.stderr)
        return False


def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Process DMCA takedown request config files and send emails.')
    parser.add_argument('config_files', nargs='+', help='Path(s) to request config file(s) (JSON format)')
    args = parser.parse_args()
    
    # Process each config file
    successful = 0
    failed = 0
    skipped = 0
    
    for config_path in args.config_files:
        result = process_config(config_path)
        if result:
            successful += 1
        else:
            if "cancelled" in str(sys.stdout):
                skipped += 1
            else:
                failed += 1
    
    # Print summary
    total = len(args.config_files)
    print(f"\n{'=' * 40}")
    print(f"DMCA Request Summary:")
    print(f"  Total requests: {total}")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Skipped: {skipped}")
    print(f"{'=' * 40}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
