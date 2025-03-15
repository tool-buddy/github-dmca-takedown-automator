#!/usr/bin/env python3
"""
DMCA Takedown Request Sender

This script processes DMCA takedown request configuration files and sends
emails to GitHub based on the configuration. Each config file should contain
all necessary information for a single DMCA request.

Usage:
    python dmca_sender.py request1.json [request2.json ...]
"""

import sys

from src.request_processor import RequestProcessor
from src.cli_handler import CLIHandler, ProcessingStats


def main() -> int:
    """
    Main entry point for the DMCA takedown request sender.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Parse command line arguments
    args = CLIHandler.parse_args()

    # Process all request files
    stats: ProcessingStats = RequestProcessor().process_batch(args.request_config_file)

    # Print summary
    print(CLIHandler.format_processing_summary(stats))

    # Return appropriate exit code
    return CLIHandler.get_exit_code(stats)


if __name__ == "__main__":
    sys.exit(main())
