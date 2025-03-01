"""
Emailing Configuration File

This file contains the configuration needed to send DMCA takedown request emails,
as well as the email template structure for GitHub DMCA Takedown Requests.

The configuration section contains SMTP server details (replace mock values with actual details).
The template section contains the structure for DMCA emails with placeholders indicated by {placeholder}.
"""


# SMTP Server Configuration
SMTP_SERVER = "mail.example.com"
SMTP_PORT = 465  # Common ports: 25 (SMTP), 465 (SMTPS), 587 (Submission)
SMTP_USERNAME = "admin@example.com"
SMTP_PASSWORD = "1234"
# Connection Security (choose one based on your SMTP_PORT)
# - For port 465: Set CONNECTION_SECURITY to "SSL"
# - For port 587: Set CONNECTION_SECURITY to "STARTTLS"
# - For port 25: Set CONNECTION_SECURITY to "NONE" (not recommended)
CONNECTION_SECURITY = "SSL"  # Options: "SSL", "STARTTLS", "NONE"

# Email Sender Configuration
FROM_EMAIL = "admin@example.com"
FROM_NAME = "Mr. Admin"
REPLY_TO = "admin@example.com"

# Optional CC recipient (set to None if not needed)
CC_EMAIL = None

# GitHub DMCA Submission
GITHUB_DMCA_EMAIL = "copyright@github.com"

# Email Template based on GitHub DMCA takedown request form
# This template contains the structure for DMCA takedown request emails to be sent to GitHub.
# Placeholders are indicated with curly braces {placeholder} and will be replaced with
# actual values from the request config files.
DMCA_EMAIL_TEMPLATE = """
Subject: DMCA Takedown Notice from {from}

Dear GitHub Team,

I, {legal_name}, am the copyright owner of content that is currently being infringed on your website. Bellow is the DMCA takedown notice submission form.

* From
{from}

* Are you the copyright holder or authorized to act on the copyright owner's behalf?
{copyright_holder_or_authorized}

* Are you submitting a revised DMCA notice after GitHub Trust & Safety requested you make changes to your original notice?
{is_revised}

* Does your claim involve content on GitHub or npm.js?
{content_source}

* Please describe the nature of your copyright ownership or authorization to act on the owner's behalf.
{ownership}

* Please provide a detailed description of the original copyrighted work that has allegedly been infringed. If possible, include a URL to where it is posted online.
{work_description}

* What files should be taken down? Please provide URLs for each file, or if the entire repository, the repository’s URL.
{infringing_urls}

* Do you claim to have any technological measures in place to control access to your copyrighted content? Please see our Complaints about Anti-Circumvention Technology if you are unsure.
{access_control}

* Have you searched for any forks of the allegedly infringing files or repositories? Each fork is a distinct repository and must be identified separately if you believe it is infringing and wish to have it taken down.
{forks_information}

* Is the work licensed under an open source license?
{open_source}

* What would be the best solution for the alleged infringement?
{solution}

* Do you have the alleged infringer’s contact information? If so, please provide it.
{contact}

* I have a good faith belief that use of the copyrighted materials described above on the infringing web pages is not authorized by the copyright owner, or its agent, or the law.
* I swear, under penalty of perjury, that the information in this notification is accurate and that I am the copyright owner, or am authorized to act on behalf of the owner, of an exclusive right that is allegedly infringed.
* I have taken fair use into consideration.
* I have read and understand GitHub's Guide to Submitting a DMCA Takedown Notice.

* So that we can get back to you, please provide either your telephone number or physical address.
{phone}

* Please type your full legal name below to sign this request.
{legal_name}

Thank you for your attention to this matter.

Sincerely,
{legal_name}
"""
