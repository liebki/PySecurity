"""Module for fetching dns record informations using the nslookup api."""

from enum import Enum
import requests
from modules.utilities import get_random_ua


class DnsProvider(Enum):
    """
    Simple DnsProvider enum, to allow to choose different provider to resolve domain.

    Args:
        Enum: d
    """

    CLOUDFLARE = "cloudflare"
    GOOGLE = "google"
    AUTHORITATIVE = "authoritative"
    CONTROLDUNFILTERED = "controldunfiltered"


def fetch_dns_records(
    domain: str,
    dns_server: DnsProvider = DnsProvider.CLOUDFLARE,
    full_response: bool = False,
):
    """
    Get the dns-records of a domain if correctly returned.

    Args:
        domain (str): The domain to query
        dns_server (DnsProvider, optional): DNS provider to use. Default is CLOUDFLARE.
        full_response (bool, optional): Return full response or selective data. Defaults to False.

    Returns:
        Depending on full_response, it returns a json structure to iterate trough.
    """

    url = "https://www.nslookup.io/api/v1/records"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-GB,en;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.nslookup.io",
        "pragma": "no-cache",
        "referer": f"https://www.nslookup.io/domains/{domain}/dns-records/",
        "user-agent": get_random_ua(),
    }
    payload = {"domain": domain, "dnsServer": dns_server.value}
    response = requests.post(url, json=payload, headers=headers, timeout=120)

    if response.status_code == 200:

        if full_response:
            return response.json()

        return __parse_dns_records(data=response.json())

    return {
        "error": f"Request failed with status code {response.status_code}",
        "details": response.text,
    }


def __parse_dns_records(data):
    """
    To return the selective json structure.

    Args:
        data: json input.

    Returns:
        The parsed json structure.
    """
    records = data.get("records", {})
    parsed_data = []

    for record_type, record_info in records.items():
        record_data = {"record_type": record_type, "answers": []}
        answers = record_info.get("response", {}).get("answer", [])

        for answer in answers:
            record = answer.get("record", {})
            raw = record.get("raw", "")
            record_data["answers"].append(
                {
                    "raw": raw,
                    "record_type": record.get("recordType", ""),
                    "name": record.get("name", ""),
                    "ttl": record.get("ttl", ""),
                }
            )

        parsed_data.append(record_data)

    return parsed_data
