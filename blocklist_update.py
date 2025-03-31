import requests
import json

BLOCKLIST_URL = "https://urlhaus.abuse.ch/downloads/text/"
TXT_FILE = "blocklist.txt"
JSON_FILE = "blocklist.json"

def fetch_latest_blocklist():
    """Fetches the latest blocklist from an external source."""
    response = requests.get(BLOCKLIST_URL)
    if response.status_code == 200:
        return set(line.strip() for line in response.text.splitlines() if line and not line.startswith("#"))
    return set()

def load_existing_blocklist():
    """Loads the current blocklist from both TXT and JSON files."""
    try:
        with open(TXT_FILE, "r") as f:
            txt_entries = set(f.read().splitlines())
    except FileNotFoundError:
        txt_entries = set()

    try:
        with open(JSON_FILE, "r") as f:
            json_data = json.load(f)
            json_entries = set(json_data.get("blocked_sites", []))
    except (FileNotFoundError, json.JSONDecodeError):
        json_entries = set()

    return txt_entries.union(json_entries)

def update_blocklists():
    """Adds new entries and updates both files."""
    new_entries = fetch_latest_blocklist()
    existing_entries = load_existing_blocklist()
    
    updated_entries = sorted(existing_entries.union(new_entries))

    # Update TXT file
    with open(TXT_FILE, "w") as f:
        f.write("\n".join(updated_entries))

    # Update JSON file
    with open(JSON_FILE, "w") as f:
        json.dump({"blocked_sites": updated_entries}, f, indent=2)

    print(f"Blocklist updated: {len(updated_entries)} domains.")

if __name__ == "__main__":
    update_blocklists()
