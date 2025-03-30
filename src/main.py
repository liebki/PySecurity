"""Main module for PySecurity - A collection of tools."""

from modules.certificate_fetcher import get_certificate_data
from modules.rdap_fetcher import (
    get_registars_rdap_endpoint,
    get_domain_contact_informations,
)
from modules.urlhaus_checker import check_existence

certificates = get_certificate_data(name="google")
print(certificates)

domain_registar_endpoint = get_registars_rdap_endpoint(tld="com")
print(domain_registar_endpoint)

domain_informations = get_domain_contact_informations(domain="pons.com", tld="com")
print(domain_informations)

elements = check_existence("27.215.212.5")
for elem in elements:
    print(elem)
