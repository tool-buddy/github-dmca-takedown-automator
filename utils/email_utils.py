"""
Email Utilities for DMCA Takedown Requests

This module provides functions for email handling, including SMTP connection,
email formatting, and sending functionality.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import sys
from emailing_config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, CONNECTION_SECURITY,
    FROM_EMAIL, FROM_NAME, REPLY_TO, GITHUB_DMCA_EMAIL, CC_EMAIL, DMCA_EMAIL_TEMPLATE
)


def format_email_content(config_data):
    """
    Format the email content based on the config data and email template.
    
    Args:
        config_data (dict): The request configuration data.
        
    Returns:
        tuple: (subject, message_body) - The formatted subject and message body.
    """
    # Extract repository names for the subject
    repositories = config_data['infringing_urls'] 
    # Format the infringing URLs list
    infringing_urls_formatted = "\n".join([f"- {url}" for url in repositories])
    
    # Create a dict with all the template variables
    template_vars = {
        'from': config_data['from'],
        'copyright_holder_or_authorized': config_data['copyright_holder_or_authorized'],
        'is_revised': config_data['is_revised'],
        'content_source': config_data['content_source'],
        'ownership': config_data['ownership'],
        'work_description': config_data['work_description'],
        'infringing_urls': infringing_urls_formatted,
        'access_control': config_data['access_control'],
        'forks_information': config_data['forks_information'],
        'open_source': config_data['open_source'],
        'solution': config_data['solution'],
        'contact': config_data['contact'],
        'legal_name': config_data['legal_name'],
        'contact_email': config_data['contact_email'],
        'phone': config_data['phone']
    }
    
    # Format the complete email using the template
    formatted_email = DMCA_EMAIL_TEMPLATE.format(**template_vars)
    
    # Extract subject from the first line
    lines = formatted_email.split('\n')
    subject = lines[1].replace('Subject:', '').strip()
    body = '\n'.join(lines[3:])  # Skip first 3 lines (empty line, subject, empty line)
    
    return subject, body


def create_email_message(config_data):
    """
    Create a MIMEMultipart email message.
    
    Args:
        config_data (dict): The request configuration data.
        
    Returns:
        MIMEMultipart: The formatted email message.
    """
    subject, body = format_email_content(config_data)
    
    message = MIMEMultipart()
    message['From'] = formataddr((FROM_NAME, FROM_EMAIL))
    message['To'] = GITHUB_DMCA_EMAIL
    message['Subject'] = subject
    message['Reply-To'] = REPLY_TO
    
    # Add CC if specified in config or global settings
    cc_email = config_data.get('cc_email', CC_EMAIL)
    if cc_email:
        message['Cc'] = cc_email
    
    message.attach(MIMEText(body, 'plain'))
    return message


def preview_email(config_data):
    """
    Generate a preview of the email that will be sent.
    
    Args:
        config_data (dict): The request configuration data.
        
    Returns:
        str: A formatted preview of the email.
    """
    subject, body = format_email_content(config_data)
    
    # Get CC email if specified in config or use global setting
    cc_email = config_data.get('cc_email', CC_EMAIL)
    cc_line = f"CC: {cc_email}" if cc_email else ""
    
    preview = f"""
{'=' * 70}
FROM: {FROM_NAME} <{FROM_EMAIL}>
TO: {GITHUB_DMCA_EMAIL}
{cc_line}
SUBJECT: {subject}
{'=' * 70}

{body}
{'=' * 70}
"""
    return preview


def send_email(config_data):
    """
    Send the DMCA takedown request email using the configured SMTP server.
    
    Args:
        config_data (dict): The request configuration data.
        
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        message = create_email_message(config_data)
        
        # Create a secure SSL/TLS context
        context = ssl.create_default_context()
        
        print(f"Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}...")
        
        # Handle different connection security types
        if CONNECTION_SECURITY == "SSL":
            # Use SMTP_SSL for secure connection (typically port 465)
            print("Using SMTP_SSL for secure connection...")
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(message)
                
        elif CONNECTION_SECURITY == "STARTTLS":
            # Use STARTTLS for secure connection (typically port 587)
            print("Using SMTP with STARTTLS...")
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(message)
                
        elif CONNECTION_SECURITY == "NONE":
            # Use plain SMTP connection (no encryption)
            print("WARNING: Using plain SMTP connection. Credentials will be sent in clear text!")
            user_ok = input("This is not secure. Continue anyway? (y/n): ").lower() in ['y', 'yes']
            if not user_ok:
                print("Email sending cancelled by user due to security concerns.")
                return False
                
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(message)
        else:
            raise ValueError(f"Invalid CONNECTION_SECURITY setting: {CONNECTION_SECURITY}. "
                             f"Must be one of: 'SSL', 'STARTTLS', or 'NONE'")
        
        print("Email sent successfully!")
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        print("Please check your SMTP_USERNAME and SMTP_PASSWORD in emailing_config.py", file=sys.stderr)
        return False
    except smtplib.SMTPConnectError as e:
        print(f"Connection to SMTP server failed: {e}", file=sys.stderr)
        print("Please check your SMTP_SERVER and SMTP_PORT in emailing_config.py", file=sys.stderr)
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}", file=sys.stderr)
        return False
    except ssl.SSLError as e:
        print(f"SSL/TLS error: {e}", file=sys.stderr)
        print("This might indicate a mismatch between your CONNECTION_SECURITY setting and what the server supports.", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error sending email: {e}", file=sys.stderr)
        return False


def get_user_confirmation():
    """
    Ask the user to confirm sending the email.
    
    Returns:
        bool: True if the user confirms, False otherwise.
    """
    while True:
        response = input("Send this email? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please answer 'y' or 'n'.")
