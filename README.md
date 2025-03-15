# GitHub DMCA Takedown Automator

A Python script for generating and sending DMCA takedown request emails to GitHub from JSON configuration files.

## Requirements

- Python 3.9+
- Pydantic 2.x+ (for configuration validation)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/tool-buddy/github-dmca-takedown-automator.git
   cd github-dmca-takedown-automator
   ```

2. Install dependencies:
   ```
   pip install pydantic
   pip install pydantic[email]
   ```



## Creating Request Config Files




## Usage

1. Update `config/emailing_config.py` with your email settings.

2. For each DMCA takedown request, create a JSON file containing the same data as the DMCA takedown notice form (https://support.github.com/contact/dmca-takedown). See `requests/example_request.json` for a template.

3. Process one or multiple requests:
```
python dmca_sender.py request1.json [request2.json ...]
```

The script will:
1. Load and validate each config file
2. Show a preview of the email
3. Ask for confirmation before sending
4. Send the email if confirmed
5. Display a summary of successful and failed requests
