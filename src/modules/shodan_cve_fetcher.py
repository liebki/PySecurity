"""Module for fetching CVE informations from the cve database endpoints of shodan."""

import requests
from modules.utilities import get_headers

SHODAN_CVES_HIGHEST_EPPS_ENDPOINT = (
    "https://cvedb.shodan.io/dashboard/highest-epss?limit=50"
)
SHODAN_CVES_BY_PRODUCT_ENDPOINT = (
    "https://cvedb.shodan.io/dashboard/vuln-by-product?limit=50"
)
SHODAN_LATEST_CVES_ENDPOINT = "https://cvedb.shodan.io/dashboard/newest?limit=50"
SHODAN_KNOWN_EXPLOITED_CVES_ENDPOINT = (
    "https://cvedb.shodan.io/dashboard/known-exploited?limit=50"
)

SHODAN_SINGLE_CVE_ENDPOINT = "https://cvedb.shodan.io/cve/"
SHODAN_CVE_BY_PRODUCT_ENDPOINT = "https://cvedb.shodan.io/cves?product="


def get_cves_by_product(product_name: str, return_full_response: bool = False):
    """
    Fetches CVEs related to a specific product from the Shodan CVE database.

    Args:
        product_name (str): The name of the product to search for vulnerabilities.
        return_full_response (bool, optional): Returns full API response. Defaults to False.

    Returns:
        list[dict] | dict: A list of CVEs with key details if return_full_response is False,
                           otherwise the full API response.
    """
    cve_list = []
    answer = requests.get(
        url=SHODAN_CVE_BY_PRODUCT_ENDPOINT + product_name,
        timeout=120,
        headers=get_headers(),
    )

    if answer.status_code == 200:
        answer_json = answer.json()

        if return_full_response:
            return answer_json

        if answer_json["cves"]:
            for cve_element in answer_json["cves"]:
                cve_details = {
                    "cve_id": cve_element["cve_id"],
                    "summary": cve_element["summary"],
                    "epss": cve_element["epss"],
                    "propose_action": cve_element["propose_action"],
                    "ransomware_campaign": cve_element["ransomware_campaign"],
                    "references": cve_element["references"],
                    "published_time": cve_element["published_time"],
                }

                cve_list.append(cve_details)

            return cve_list

    return []


def get_cve_informations(cve_id: str, return_full_response: bool = False):
    """
    Retrieves detailed information about a specific CVE.

    Args:
        cve_id (str): The CVE identifier (e.g., CVE-2024-1234).
        return_full_response (bool, optional): Returns full API response. Defaults to False.

    Returns:
        dict: A dictionary containing CVE details if found, otherwise an empty dictionary.
    """
    cve_details = {}
    answer = requests.get(
        url=SHODAN_SINGLE_CVE_ENDPOINT + cve_id, timeout=60, headers=get_headers()
    )

    if answer.status_code == 200:
        answer_json = answer.json()

        if return_full_response:
            return answer_json

        cve_details.update(
            {
                "summary": answer_json["summary"],
                "epss": answer_json["epss"],
                "propose_action": answer_json["propose_action"],
                "ransomware_campaign": answer_json["ransomware_campaign"],
                "published_time": answer_json["published_time"],
                "references": answer_json["references"],
            }
        )
        return cve_details

    return {}


def get_latest_cves():
    """
    Fetches the latest CVEs from the Shodan CVE database.

    Returns:
        list[dict]: A list of dictionaries containing the latest CVEs and their components.
    """
    cve_list = []
    answer = requests.get(
        url=SHODAN_LATEST_CVES_ENDPOINT, timeout=60, headers=get_headers()
    )

    if answer.status_code == 200:
        answer_json = answer.json()
        for cve_element in answer_json:
            cve_item = {
                "cve_id": cve_element["cve_id"],
                "components": cve_element["components"],
            }
            cve_list.append(cve_item)

        return cve_list

    return []


def get_known_exploited_cves():
    """
    Retrieves a list of known exploited CVEs.

    Returns:
        list[dict]: A list of dictionaries containing known exploited CVEs and their components.
    """
    cve_list = []
    answer = requests.get(
        url=SHODAN_KNOWN_EXPLOITED_CVES_ENDPOINT, timeout=60, headers=get_headers()
    )

    if answer.status_code == 200:
        answer_json = answer.json()
        for cve_element in answer_json:
            cve_item = {
                "cve_id": cve_element["cve_id"],
                "components": cve_element["components"],
            }
            cve_list.append(cve_item)

        return cve_list

    return []


def get_cves_with_highest_epps():
    """
    Fetches CVEs with the highest EPSS (Exploit Prediction Scoring System) scores.

    Returns:
        list[dict]: A list of dictionaries containing CVEs with their EPSS scores and components.
    """
    cve_list = []
    answer = requests.get(
        url=SHODAN_CVES_HIGHEST_EPPS_ENDPOINT, timeout=60, headers=get_headers()
    )

    if answer.status_code == 200:
        answer_json = answer.json()
        for cve_element in answer_json:
            cve_item = {
                "cve_id": cve_element["cve_id"],
                "epss_score": cve_element["epss"],
                "components": cve_element["components"],
            }

            cve_list.append(cve_item)

        return cve_list

    return []
