# Blocklist for Malicious Websites

This repository provides a list of known malicious websites to help users block harmful domains and enhance security. The list can be used with firewalls, DNS filters, and adblockers like Pi-hole and AdGuard.

## Usage

### Plain Text Blocklist
- The `blocklist.txt` file contains a simple list of domains, one per line.
- Example:
  ```
  badwebsite.com
  malware-site.net
  phishing-site.org
  ```
- Compatible with Pi-hole, AdGuard Home, and similar filtering solutions.

### JSON Format
- The `blocklist.json` file provides the data in structured JSON format:
  ```json
  {
    "blocked_sites": [
      "badwebsite.com",
      "malware-site.net"
    ]
  }
  ```
- Useful for applications that require structured input.

## How to Contribute
- If you find a malicious website that is not on the list, feel free to submit a pull request.
- Open an issue if a site is mistakenly included.

## Disclaimer
This blocklist is provided as-is with no guarantees. Always use additional security measures and perform your own due diligence when using blocklists.

