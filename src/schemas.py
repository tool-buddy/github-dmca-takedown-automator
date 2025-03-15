"""
Schema Definitions for DMCA Takedown Requests

This module contains type definitions and validation rules for the DMCA
takedown request automation system. These schemas define the structure
of configuration files.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class RequestConfig(BaseModel):
    """Class defining the structure of a DMCA takedown request configuration."""

    from_: str = Field(
        ..., alias="from"
    )  # Using alias to handle Python keyword conflict
    copyright_holder_or_authorized: str
    is_revised: Literal["Yes", "No"]
    content_source: Literal["GitHub", "npm.js", "Both"]
    ownership: str
    work_description: str
    infringing_urls: List[str]
    access_control: Literal["Yes", "No"]
    forks_information: str
    open_source: Literal["Yes", "No"]
    solution: str
    contact: str
    legal_name: str
    phone: str

    class Config:
        """Pydantic model configuration."""

        populate_by_name = True  # Allow both alias and field name to be used
        validate_assignment = True  # Validate on assignment
        extra = "forbid"  # Forbid extra fields not specified in the model


class SmtpConfig(BaseModel):
    """SMTP server configuration."""

    server: str
    port: int
    """The SMTP server address. Common ports: 25 (SMTP), 465 (SMTPS), 587 (Submission)"""
    username: str
    password: str
    connection_security: Literal["SSL", "STARTTLS", "NONE"]
    """Connection security settings:
    - For port 465: Set to "SSL"
    - For port 587: Set to "STARTTLS"
    - For port 25: Set to "NONE" (not recommended)"""


class AddressingConfig(BaseModel):
    """Email addressing configuration."""

    from_email: EmailStr
    from_name: str
    reply_to: Optional[EmailStr]
    cc_email: Optional[EmailStr]
    to_email: EmailStr


class EmailConfig(BaseModel):
    """Class to store email service configuration."""

    smtp: SmtpConfig
    addressing: AddressingConfig
    email_template: str
    """Email Template based on GitHub DMCA takedown request form
    This template contains the structure for DMCA takedown request emails to be sent to GitHub.
    Placeholders are indicated with curly braces {placeholder} and will be replaced with
    actual values from the request config files."""
