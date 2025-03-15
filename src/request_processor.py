"""
Processes DMCA takedown request files.

Handles batch processing of DMCA takedown requests by loading configuration,
validating user data, formatting emails, and sending them through the EmailService.
Includes error handling and reporting for each request processed.
"""

from pathlib import Path
import sys
from typing import List

from src.cli_handler import CLIHandler, ProcessingResult, ProcessingStats
from src.config_loader import load_request_config
from src.email_service import EmailService, get_user_confirmation
from src.exceptions import ConfigError, DMCAError, EmailError
from src.schemas import RequestConfig
from config.emailing_config import EMAIL_CONFIG

class RequestProcessor:
    """
    Handles the processing of DMCA takedown request files.

    This class coordinates the loading of config files, validation,
    email formatting and sending, and user interaction.
    """

    def __init__(self) -> None:
        """
        Initialize the request processor.
        """
        self.email_service = EmailService(EMAIL_CONFIG)

    def process_request(self, request_file: str) -> ProcessingResult:
        """
        Process a single DMCA takedown request config file.

        Args:
            request_file: Path to the request config file

        Returns:
            ProcessingResult with the outcome of processing
        """
        try:
            # Get filename for reporting
            filename = Path(request_file).name
            print(f"\nProcessing config file: {request_file}")

            # Load and validate the config
            config: RequestConfig = load_request_config(request_file)

            # Generate and show email preview
            print(self.email_service.generate_preview(config))

            # Get user confirmation
            if not get_user_confirmation():
                print("Email sending cancelled by user.")
                return ProcessingResult(filename=filename, status="SKIPPED")

            # Send the email
            self.email_service.send(config)
            print(f"Successfully sent DMCA takedown request for {filename}")
            return ProcessingResult(filename=filename, status="SUCCESS")

        except ConfigError as e:
            error_msg = f"Configuration error: {e}"
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return ProcessingResult(
                filename=Path(request_file).name,
                status="FAILED",
                error_message=error_msg,
            )
        except EmailError as e:
            error_msg = f"Email error: {e}"
            print(f"ERROR: {error_msg}", file=sys.stderr)

            # Add context details if available
            if hasattr(e, "context") and e.context:
                context_str = "\n".join(f"  {k}: {v}" for k, v in e.context.items())
                print(f"Context:\n{context_str}", file=sys.stderr)

            return ProcessingResult(
                filename=Path(request_file).name,
                status="FAILED",
                error_message=error_msg,
            )
        except DMCAError as e:
            error_msg = f"Error: {e}"
            print(f"ERROR: {error_msg}", file=sys.stderr)
            return ProcessingResult(
                filename=Path(request_file).name,
                status="FAILED",
                error_message=error_msg,
            )

    def process_batch(self, request_files: List[str]) -> ProcessingStats:
        """
        Process multiple DMCA takedown request config files.

        Args:
            request_files: List of paths to request config files

        Returns:
            ProcessingStats with batch processing statistics
        """
        stats = ProcessingStats()

        for request_file in request_files:
            result = self.process_request(request_file)
            stats.add_result(result)
            CLIHandler.print_result_status(result)

        return stats
