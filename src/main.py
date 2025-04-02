"""Main module for PySecurity - A collection of tools."""

from modules.certificate_fetcher import get_certificate_data
from modules.rdap_fetcher import (
    get_registars_rdap_endpoint,
    get_domain_contact_informations,
)
from modules.urlhaus_checker import check_existence
from modules.ip_info_fetcher import get_ip_informations
from modules.shodan_cve_fetcher import (
    get_cves_by_product,
    get_cve_informations,
    get_cves_with_highest_epps,
    get_known_exploited_cves,
    get_latest_cves,
)
from modules.dns_nslookup_fetcher import fetch_dns_records, DnsProvider


certificates = get_certificate_data(name="google")
print(certificates)

domain_registar_endpoint = get_registars_rdap_endpoint(tld="com")
print(domain_registar_endpoint)

domain_informations = get_domain_contact_informations(domain="pons.com", tld="com")
print(domain_informations)

elements = check_existence("27.215.212.5")
for elem in elements:
    print(elem)

ip_informations = get_ip_informations(ip="12.82.121.191")
print(ip_informations)

cve_list_product = get_cves_by_product(product_name="chrome")
for cve in cve_list_product:
    print(cve)
    print("\n")


cve_latest = get_latest_cves()
for cve in cve_latest:
    print(cve)


cve_epps = get_cves_with_highest_epps()
for cve in cve_epps:
    print(cve)

known_exploited_cves = get_known_exploited_cves()
for ke_cve in known_exploited_cves:
    print(ke_cve)


cve_data = get_cve_informations(cve_id="CVE-2016-10087")
print(cve_data)

record_daten = fetch_dns_records(domain="chip.de", dns_server=DnsProvider.GOOGLE)

for record in record_daten:
    print(f"Record Type: {record['record_type']}")
    for answer in record["answers"]:
        print(f"  Raw: {answer['raw']}")
        print(f"  Record Type: {answer['record_type']}")
        print(f"  Name: {answer['name']}")
        print(f"  TTL: {answer['ttl']}")
