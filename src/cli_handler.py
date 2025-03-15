"""
Command Line Interface Handler for DMCA Takedown Requests

This module provides a CLI handler for processing DMCA takedown requests,
including argument parsing, user interaction, and result reporting.
"""

import argparse
from dataclasses import dataclass
from typing import Optional, Dict, Literal, Any


@dataclass
class ProcessingResult:
    """Class to store the result of processing a single request."""

    filename: str
    status: Literal["SUCCESS", "FAILED", "SKIPPED"]
    error_message: Optional[str] = None


@dataclass
class ProcessingStats:
    """Class to store statistics for batch processing."""

    total: int = 0
    successful: int = 0
    failed: int = 0
    skipped: int = 0

    def add_result(self, result: ProcessingResult) -> None:
        """Add a processing result to the statistics."""
        self.total += 1
        if result.status == "SUCCESS":
            self.successful += 1
        elif result.status == "SKIPPED":
            self.skipped += 1
        elif result.status == "FAILED":
            self.failed += 1
        else:
            raise ValueError(f"Invalid result status: {result.status}")


class CLIHandler:
    """Handler for CLI operations in the DMCA takedown request tool."""

    @staticmethod
    def parse_args() -> argparse.Namespace:
        """
        Parse command line arguments.

        Returns:
            Parsed arguments namespace
        """
        parser = argparse.ArgumentParser(
            description="Process DMCA takedown request config files and send emails.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python dmca_sender.py requests/my_request.json
  python dmca_sender.py requests/request1.json requests/request2.json
            """,
        )

        parser.add_argument(
            "request_config_file",
            nargs="+",
            help="Path(s) to request config file(s) (JSON format)",
        )
        return parser.parse_args()

    @staticmethod
    def format_processing_summary(stats: ProcessingStats) -> str:
        """
        Format processing statistics into a readable summary.

        Args:
            stats: Processing statistics

        Returns:
            Formatted summary string
        """
        return f"""
{'=' * 60}
DMCA REQUEST PROCESSING SUMMARY
{'=' * 60}
Total requests:  {stats.total}
Successful:     {stats.successful}
Failed:         {stats.failed}
Skipped:        {stats.skipped}
{'=' * 60}
"""

    @staticmethod
    def format_error(
        error_message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Format an error message with optional context information.

        Args:
            error_message: The main error message
            context: Optional context information

        Returns:
            Formatted error string
        """
        result = f"ERROR: {error_message}"

        if context:
            context_str = "\n".join(f"  {k}: {v}" for k, v in context.items())
            result += f"\nContext:\n{context_str}"

        return result

    @staticmethod
    def print_result_status(result: ProcessingResult) -> None:
        """
        Print the status of a single request processing result.

        Args:
            result: The processing result
        """

        print(f"[{result.status}] {result.filename}")

        if result.error_message and not result.status == "FAILED":
            print(f"  → {result.error_message}")

    @staticmethod
    def get_exit_code(stats: ProcessingStats) -> int:
        """
        Determine the appropriate exit code based on processing results.

        Args:
            stats: Processing statistics

        Returns:
            Exit code (0 for success, 1 for failures)
        """
        return 0 if stats.failed == 0 else 1
