#!/usr/bin/env python3
"""
FreelanceFlow — Notion API Client
Feeds job descriptions into Notion's Client Pipeline database,
triggering the FreelanceFlow Custom Agent automatically.

Usage:
    python notion_freelanceflow.py --brief "Need a Python scraper..."
    python notion_freelanceflow.py --file brief.txt
    python notion_freelanceflow.py --interactive

Setup:
    1. Create a Notion internal integration: https://www.notion.so/profile/integrations
    2. Set NOTION_MCP_TOKEN to your integration secret in .env
    3. Set NOTION_DATABASE_ID to your Client Pipeline database ID
    4. Share the Client Pipeline database with your integration
    5. pip install httpx python-dotenv

Notion API: https://api.notion.com/v1
Rate limits: 3 req/sec
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

import httpx
from dotenv import load_dotenv

load_dotenv()

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_MCP_TOKEN = os.getenv("NOTION_MCP_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"


def notion_request(method: str, path: str, body: dict | None = None) -> dict:
    """Make an authenticated Notion API request."""
    if not NOTION_MCP_TOKEN:
        raise EnvironmentError(
            "NOTION_MCP_TOKEN not set. "
            "Create an integration at https://www.notion.so/profile/integrations"
        )

    headers = {
        "Authorization": f"Bearer {NOTION_MCP_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
    }

    with httpx.Client(timeout=30) as client:
        if method == "POST":
            response = client.post(
                f"{NOTION_API_URL}{path}", json=body, headers=headers
            )
        else:
            response = client.get(f"{NOTION_API_URL}{path}", headers=headers)
        response.raise_for_status()
        return response.json()


def find_database(name_hint: str = "Client Pipeline") -> str | None:
    """Search for the Client Pipeline database by name."""
    result = notion_request("POST", "/search", {
        "query": name_hint,
        "filter": {"value": "database", "property": "object"},
    })
    results = result.get("results", [])
    if results:
        return results[0]["id"]
    return None


def create_pipeline_entry(brief: str, database_id: str) -> dict:
    """Create a new entry in the Client Pipeline database."""
    now = datetime.now(timezone.utc).isoformat()

    return notion_request("POST", "/pages", {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": f"New Brief — {now[:10]}"}}
                ]
            },
            "Status": {
                "select": {"name": "New Brief"}
            },
            "Brief": {
                "rich_text": [
                    {"text": {"content": brief}}
                ]
            },
            "Date Added": {
                "date": {"start": now}
            },
        },
    })


def get_page_url(page_id: str) -> str:
    """Build the Notion page URL from a page ID."""
    clean_id = page_id.replace("-", "")
    return f"https://www.notion.so/{clean_id}"


def main():
    parser = argparse.ArgumentParser(
        description="FreelanceFlow — Feed client briefs into Notion via MCP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", help="Client brief text (inline)")
    group.add_argument("--file", help="Path to a .txt file containing the brief")
    group.add_argument(
        "--interactive", action="store_true", help="Enter brief interactively"
    )
    parser.add_argument(
        "--database-id",
        default=DATABASE_ID,
        help="Notion database ID (overrides env var NOTION_DATABASE_ID)",
    )
    args = parser.parse_args()

    # Resolve brief text
    if args.brief:
        brief = args.brief
    elif args.file:
        with open(args.file) as f:
            brief = f.read().strip()
    else:
        print("Paste the client brief below. Press Enter twice when done:\n")
        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        brief = "\n".join(lines).strip()

    if not brief:
        print("Error: Brief is empty.", file=sys.stderr)
        sys.exit(1)

    # Resolve database ID
    db_id = args.database_id
    if not db_id:
        print("No NOTION_DATABASE_ID set — searching workspace for 'Client Pipeline'...")
        db_id = find_database("Client Pipeline")
        if not db_id:
            print(
                "Error: Could not find 'Client Pipeline' database. "
                "Set NOTION_DATABASE_ID in .env or pass --database-id.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"Found database: {db_id}")

    # Create the entry
    print(f"\nCreating Client Pipeline entry...")
    print(f"Brief preview: {brief[:80]}{'...' if len(brief) > 80 else ''}\n")

    entry = create_pipeline_entry(brief, db_id)
    page_id = entry.get("id", "unknown")
    notion_url = entry.get("url", get_page_url(page_id) if page_id != "unknown" else "(check Notion)")
    url = notion_url

    print("✅ Entry created successfully!")
    print(f"   Page ID: {page_id}")
    print(f"   URL: {url}")
    print(f"\nFreelanceFlow agent will generate your documents automatically.")
    print("Check the 'Documents Ready' status in Notion in a few moments.")


if __name__ == "__main__":
    main()
