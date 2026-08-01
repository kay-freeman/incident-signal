import argparse
import json
from pathlib import Path

from .detection import detect_incidents
from .ingestion import load_tickets
from .reporting import (
    build_json_report,
    build_text_report,
    save_report,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TICKET_FILE = PROJECT_ROOT / "data" / "sample_tickets.json"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect incident patterns across support tickets."
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_TICKET_FILE,
        help="Path to a JSON ticket file.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=3,
        help="Minimum number of related tickets required (default: 3).",
    )

    parser.add_argument(
        "--window",
        type=int,
        default=30,
        help="Detection window in minutes (default: 30).",
    )

    parser.add_argument(
        "--format",
        dest="output_format",
        choices=("text", "json"),
        default="text",
        help="Report format: text or json (default: text).",
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path where the report will be saved.",
    )

    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()

    try:
        tickets = load_tickets(arguments.input)
        incidents = detect_incidents(
            tickets,
            threshold=arguments.threshold,
            window_minutes=arguments.window,
        )
    except FileNotFoundError:
        raise SystemExit(
            f"Error: Input file not found: {arguments.input}"
        )
    except json.JSONDecodeError as error:
        raise SystemExit(
            f"Error: Invalid JSON in {arguments.input} "
            f"at line {error.lineno}, column {error.colno}."
        )
    except ValueError as error:
        raise SystemExit(f"Error: {error}")

    report_arguments = {
        "input_file": arguments.input,
        "tickets_analyzed": len(tickets),
        "incidents": incidents,
        "threshold": arguments.threshold,
        "window_minutes": arguments.window,
    }

    if arguments.output_format == "json":
        report_content = build_json_report(**report_arguments)
    else:
        report_content = build_text_report(**report_arguments)

    if arguments.output:
        try:
            saved_path = save_report(
                report_content,
                arguments.output,
            )
        except OSError as error:
            raise SystemExit(
                f"Error: Could not save report to "
                f"{arguments.output}: {error}"
            )

        print(f"Report saved to: {saved_path}")
        return

    print(report_content)


if __name__ == "__main__":
    main()