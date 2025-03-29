"""Main module for PySecurity - A collection of tools."""

import requests
import json
from certificate_fetcher import get_certificate_data
from rdap_fetcher import get_registars_rdap_endpoint, get_domain_contact_informations

certificates = get_certificate_data("google")
print(certificates)

domain_informations = get_domain_contact_informations("pons.com", "com")
print(domain_informations)