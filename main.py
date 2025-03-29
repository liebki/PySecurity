"""Main module for PySecurity - A collection of tools."""

from certificate_fetcher import get_certificate_data
from rdap_fetcher import get_registars_rdap_endpoint, get_domain_contact_informations

certificates = get_certificate_data(name="google")
print(certificates)

domain_registar_endpoint = get_registars_rdap_endpoint(tld="com")
print(domain_registar_endpoint)

domain_informations = get_domain_contact_informations(domain="pons.com", tld="com")
print(domain_informations)
