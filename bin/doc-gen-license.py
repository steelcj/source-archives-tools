#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate SAT-compliant license block for documentation.

Usage:
    python generate_sat_license.py "Your Document Title"

Output:
    Prints the license block to stdout.
    Optionally saves to file with --output FILENAME.
"""

import sys
import argparse
from pathlib import Path


def generate_license(document_title: str) -> str:
    """Generate SAT license block with dynamic document title."""
    license_block = f"""## License

© 2024–2025 Christopher Steel.

This document, ***{document_title}***, by **Christopher Steel**, with documentation assistance from **[Euria (Infomaniak)](https://www.infomaniak.com/en/euria)**, is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**.

![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

> **About Euria**:  
> [Euria (Infomaniak)](https://www.infomaniak.com/en/euria) is an ethical, Swiss-hosted, open-source-based AI assistant focused on privacy, ecology, and technological independence."""
    return license_block


def main():
    parser = argparse.ArgumentParser(
        description="Generate SAT-compliant license block for documentation."
    )
    parser.add_argument(
        "title",
        type=str,
        help="Title of the document (will replace [DOCUMENT_TITLE])"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional: Save output to file instead of printing to stdout"
    )

    args = parser.parse_args()

    license_text = generate_license(args.title)

    if args.output:
        output_path = Path(args.output)
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent dirs if needed
            output_path.write_text(license_text, encoding="utf-8", newline="\n")
            print(f"✅ License block saved to {output_path.resolve()}")
        except Exception as e:
            print(f"❌ Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(license_text)


if __name__ == "__main__":
    main()
