import requests
import json

# Sources for malicious domains
SOURCES = [
    "https://urlhaus.abuse.ch/downloads/text/",
    "https://data.phishtank.com/data/online-valid.csv"
]

TXT_FILE = "blocklist.txt"
JSON_FILE = "blocklist.json"

def fetch_latest_blocklist():
    """Fetches and aggregates the latest blocklists from multiple sources."""
    domains = set()
    
    for url in SOURCES:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                if url.endswith(".csv"):
                    # Extract domains from CSV (PhishTank format)
                    lines = response.text.splitlines()
                    for line in lines[1:]:  # Skip header
                        parts = line.split(",")
                        if len(parts) > 1:
                            domain = parts[1].strip().replace('"', '')
                            if domain:
                                domains.add(domain)
                else:
                    # Extract domains from plaintext sources
                    for line in response.text.splitlines():
                        line = line.strip()
                        if line and not line.startswith("#"):
                            domains.add(line)
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")

    return domains

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
    """Merges new entries, removes duplicates, and updates both files."""
    new_entries = fetch_latest_blocklist()
    existing_entries = load_existing_blocklist()
    
    updated_entries = sorted(existing_entries.union(new_entries))  # Remove duplicates and sort

    # Update TXT file
    with open(TXT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_entries))

    # Update JSON file
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump({"blocked_sites": updated_entries}, f, indent=2)


    print(f"Blocklist updated: {len(updated_entries)} domains.")

if __name__ == "__main__":
    update_blocklists()
