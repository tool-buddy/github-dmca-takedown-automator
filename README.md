# Github DMCA Takedown Automator

A Python script for generating and sending DMCA takedown request emails to GitHub from JSON configuration files.

## Setup

Setup the emailing configuration and customize the email template in [emailing_config.py](./emailing_config.py).

## Creating Request Config Files

For each DMCA takedown request, create a JSON file containing the same data as the [DMCA takedown notice form](https://support.github.com/contact/dmca-takedown). See [example_request.json](./requests/example_request.json) for a template.

## Usage

To process one or multiple request config files and send emails:

```
python dmca_sender.py requests/request1.json requests/request2.json
```

The script will:
1. Load and validate each config file
2. Show a preview of the email
3. Ask for confirmation before sending
4. Send the email if confirmed
5. Display a summary of successful and failed requests
