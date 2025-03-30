# PySecurity

## Overview
This projects is/will provide a bunch of stuff to get informations that are publicly available or network related functionality.

1. **Fetching SSL Certificate Data**: Queries `crt.sh` to obtain SSL certificate transparency logs.
2. **Fetching Domain Registrar and Contact Information**: Uses the IANA RDAP service to retrieve registrar details and contact information for a given domain.
3. **UrlHaus URL Check**: Check a url, domain, IP or whatever against the database of UrlHaus.

## Features
This project aims to include the following features:
- **Fetch SSL certificate information**
- **Retrieve domain informations for a given domain using RDAP** (see Notes)
  - Get domain contact details, including registrar information, phone numbers, and emails
  - Extract domain registration events (e.g., creation and expiration dates)
  - The name (often the registrar or company where the domain was purchased)
- **Use the UrlHaus database to check a url, domain or IP**
  - If found in dataset, further information like urlhaus-link, date of addition, threat and exact threat-url are returned.


### Planned:
  - Shodan crawling for host and service enumeration
  - AbuseIP database checks for malicious IPs
    - Maybe as API-Key is needed
  - IP information retrieval (e.g., geolocation, ASN data)
  - Network scanning capabilities
  - CVE (Common Vulnerabilities and Exposures) information lookup
  - Other security and reconnaissance utilities as needed

## Requirements
- Python 3.x
- `requests` library

## Installation
To install the required dependencies, run:
```sh
pip install requests
```

## Usage
- Please check the `main.py` file for the code or the individual modules in the `modules` folder.


## Notes
- Some domains may not have publicly available contact information due to privacy regulations.
- Some TLDs, especially country-code TLDs (ccTLDs), may not have an RDAP instance available.
  - Example: `.de` domains do not work since DENIC does not provide an RDAP instance.
- If no data is available, functions return `None`.

## License
This project is open-source and available under the MIT License.
