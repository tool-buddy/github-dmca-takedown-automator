"""
Email Service for DMCA Takedown Requests

This module provides an EmailService class for handling email operations,
including formatting, previewing, and sending DMCA takedown notices.
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from typing import Dict
from dataclasses import dataclass

from src.schemas import RequestConfig, EmailConfig, AddressingConfig
from src.exceptions import EmailError


@dataclass
class EmailContent:
    """Class to store the formatted content of an email."""

    subject: str
    body: str


class EmailService:
    """Service for handling DMCA takedown email operations."""

    def __init__(self, config: EmailConfig):
        """
        Initialize the email service with configuration.

        Args:
            config: Email service configuration. If None, default values will be used.
        """
        self.config = config

    def format_email_content(self, config: RequestConfig) -> EmailContent:
        """
        Format the email content based on the config data and email template.

        Args:
            config: The request configuration data.

        Returns:
            EmailContent object with formatted subject and body.
        """
        # Format the infringing URLs list
        infringing_urls_formatted: str = "\n".join(
            [f"- {url}" for url in config.infringing_urls]
        )

        # Create a dict with all the template variables
        template_vars: Dict[str, str] = {
            "from": config.from_,
            "copyright_holder_or_authorized": config.copyright_holder_or_authorized,
            "is_revised": config.is_revised,
            "content_source": config.content_source,
            "ownership": config.ownership,
            "work_description": config.work_description,
            "infringing_urls": infringing_urls_formatted,
            "access_control": config.access_control,
            "forks_information": config.forks_information,
            "open_source": config.open_source,
            "solution": config.solution,
            "contact": config.contact,
            "legal_name": config.legal_name,
            "phone": config.phone,
        }

        try:
            # Format the complete email using the template
            formatted_email: str = self.config.email_template.format(**template_vars)

            # Extract subject from the first line
            lines = formatted_email.split("\n")
            subject: str = lines[1].replace("Subject:", "").strip()
            body: str = "\n".join(lines[3:])  # Skip first 3 lines

            return EmailContent(subject=subject, body=body)
        except KeyError as e:
            raise EmailError(f"Missing template variable: {e}") from e
        except Exception as e:
            raise EmailError(f"Error formatting email content: {e}") from e

    def create_email_message(self, config: RequestConfig) -> MIMEMultipart:
        """
        Create a MIMEMultipart email message.

        Args:
            config: The request configuration data.

        Returns:
            The formatted email message.
        """
        email_content = self.format_email_content(config)
        addressing_config: AddressingConfig = self.config.addressing

        message = MIMEMultipart()
        message["From"] = formataddr(
            (addressing_config.from_name, addressing_config.from_email)
        )
        message["To"] = addressing_config.to_email
        message["Subject"] = email_content.subject
        if addressing_config.reply_to:
            message["Reply-To"] = addressing_config.reply_to
        if addressing_config.cc_email:
            message["Cc"] = addressing_config.cc_email

        message.attach(MIMEText(email_content.body, "plain"))
        return message

    def generate_preview(self, config: RequestConfig) -> str:
        """
        Generate a preview of the email that will be sent.

        Args:
            config: The request configuration data.

        Returns:
            A formatted preview of the email.
        """
        email_content = self.format_email_content(config)
        addressing_config: AddressingConfig = self.config.addressing

        # Get CC email from global setting
        cc_email = addressing_config.cc_email
        cc_line: str = f"CC: {cc_email}" if cc_email else ""

        preview: str = f"""
{'=' * 70}
FROM: {addressing_config.from_name} <{addressing_config.from_email}>
TO: {addressing_config.to_email}
{cc_line}
SUBJECT: {email_content.subject}
{'=' * 70}

{email_content.body}
{'=' * 70}
"""
        return preview

    def send(self, config: RequestConfig, skip_confirmation: bool = False) -> bool:
        """
        Send the DMCA takedown request email.

        Args:
            config: The request configuration data.
            skip_confirmation: Whether to skip user confirmation for insecure connections.

        Returns:
            True if the email was sent successfully, False otherwise.

        Raises:
            EmailError: If there's an error during the email sending process.
        """
        try:
            message = self.create_email_message(config)

            # Create a secure SSL/TLS context
            context = ssl.create_default_context()

            smtp_config = self.config.smtp
            print(
                f"Connecting to SMTP server {smtp_config.server}:{smtp_config.port}..."
            )

            # Handle different connection security types
            if smtp_config.connection_security == "SSL":
                # Use SMTP_SSL for secure connection (typically port 465)
                print("Using SMTP_SSL for secure connection...")
                with smtplib.SMTP_SSL(
                    smtp_config.server, smtp_config.port, context=context
                ) as server:
                    server.login(smtp_config.username, smtp_config.password)
                    server.send_message(message)

            elif smtp_config.connection_security == "STARTTLS":
                # Use STARTTLS for secure connection (typically port 587)
                print("Using SMTP with STARTTLS...")
                with smtplib.SMTP(smtp_config.server, smtp_config.port) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(smtp_config.username, smtp_config.password)
                    server.send_message(message)

            elif smtp_config.connection_security == "NONE":
                # Use plain SMTP connection (no encryption)
                print(
                    "WARNING: Using plain SMTP connection. Credentials will be sent in clear text!"
                )

                if not skip_confirmation:
                    user_ok: bool = input(
                        "This is not secure. Continue anyway? (y/n): "
                    ).lower() in ["y", "yes"]
                    if not user_ok:
                        print(
                            "Email sending cancelled by user due to security concerns."
                        )
                        return False

                with smtplib.SMTP(smtp_config.server, smtp_config.port) as server:
                    server.login(smtp_config.username, smtp_config.password)
                    server.send_message(message)

            print("Email sent successfully!")
            return True

        except smtplib.SMTPAuthenticationError as e:
            error_context = {
                "server": self.config.smtp.server,
                "port": self.config.smtp.port,
            }
            raise EmailError(
                f"Authentication failed: {e}. Check SMTP_USERNAME and SMTP_PASSWORD.",
                error_context,
            ) from e
        except smtplib.SMTPConnectError as e:
            error_context = {
                "server": self.config.smtp.server,
                "port": self.config.smtp.port,
            }
            raise EmailError(
                f"Connection to SMTP server failed: {e}. Check SMTP_SERVER and SMTP_PORT.",
                error_context,
            ) from e
        except smtplib.SMTPException as e:
            raise EmailError(f"SMTP error: {e}") from e
        except ssl.SSLError as e:
            raise EmailError(
                f"SSL/TLS error: {e}. This might indicate a mismatch between your "
                f"CONNECTION_SECURITY setting and what the server supports."
            ) from e
        except Exception as e:
            raise EmailError(f"Error sending email: {e}") from e


def get_user_confirmation() -> bool:
    """
    Ask the user to confirm sending the email.

    Returns:
        True if the user confirms, False otherwise.
    """
    while True:
        response: str = input("Send this email? (y/n): ").strip().lower()
        if response in ["y", "yes"]:
            return True
        if response in ["n", "no"]:
            return False
        print("Please answer 'y' or 'n'.")
