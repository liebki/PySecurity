# PySecurity

## Overview
This projects is/will provide a bunch of stuff to get informations that are publicly available or network related functionality.

1. **Fetching SSL Certificate Data**: Queries `crt.sh` to obtain SSL certificate transparency logs.
2. **Fetching Domain Registrar and Contact Information**: Uses the IANA RDAP service to retrieve registrar details and contact information for a given domain.

## Features
This project aims to include the following features:
- Fetch SSL certificate information using `crt.sh`
- Retrieve RDAP registrar endpoint for a given TLD
- Get domain contact details, including registrar information, phone numbers, and emails
- Extract domain registration events (e.g., creation and expiration dates)
- If a domain is listed and data is available, the script prints:
  - The name (often the registrar or company where the domain was purchased)
  - The phone and email contact details
  - Domain events such as registration, expiration, and last change dates


### Planned:
  - Shodan crawling for host and service enumeration
  - AbuseIP database checks for malicious IPs
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
### 1. Get SSL Certificate Data
```python
from certificate_fetcher import get_certificate_data

cert_data = get_certificate_data("example.com")
print(cert_data)
```
**Output:** JSON response containing SSL certificate details.

### 2. Get Registrar RDAP Endpoint
```python
from rdap_fetcher import get_registars_rdap_endpoint

tld = "com"
rdap_url = get_registars_rdap_endpoint(tld)
print(rdap_url)
```
**Output:** RDAP endpoint URL for the given TLD (if available).

### 3. Get Domain Contact Information
```python
from rdap_fetcher import get_domain_contact_informations

domain = "example"
tld = "com"
domain_info = get_domain_contact_informations(domain, tld)
print(domain_info)
```
**Output:** JSON containing domain contact details (name, phone, email) and registration events.

## Notes
- Some domains may not have publicly available contact information due to privacy regulations.
- Some TLDs, especially country-code TLDs (ccTLDs), may not have an RDAP instance available.
  - Example: `.de` domains do not work since DENIC does not provide an RDAP instance.
- If no data is available, functions return `None`.

## License
This project is open-source and available under the MIT License.
