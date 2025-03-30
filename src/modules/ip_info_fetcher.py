"""Module for information retrieval about IP's from different providers."""

import requests

FREEAPIAPI_ENDPOINT = "https://freeipapi.com/api/json/"
IPWHOIS_ENDPOINT = "https://ipwho.is/"
IPGEO_TECHNIKNEWS = "https://api.techniknews.net/ipgeo/"


def __get_ipapi_url(ip: str) -> str:
    """
    Constructs the URL for the ipapi.co API endpoint.

    Args:
        ip (str): The IP address to query.

    Returns:
        str: The complete URL for the ipapi.co API.
    """
    return f"https://ipapi.co/{ip}/json/"


def get_ip_informations(ip: str):
    """
    Retrieves and merges IP information from multiple APIs.

    Args:
        ip (str): The IP address to lookup.

    Returns:
        dict: A dictionary containing merged IP information from various APIs.
              The keys are the data fields, and the values are lists of unique
              values obtained from the APIs.
    """
    techniknews_data = __call_techniknews_api(ip=ip)
    ipapi_data = __call_ipapi_api(ip=ip)
    ipwhois_data = __call_ipwhois_api(ip=ip)
    freeipapi_data = __call_freeipapi_api(ip=ip)

    dicts = [
        d for d in [techniknews_data, ipapi_data, ipwhois_data, freeipapi_data] if d
    ]
    merged_data = {}

    for d in dicts:
        for key, value in d.items():
            if key in merged_data:
                merged_data[key].add(value)
            else:
                merged_data[key] = {value}

    final_data = {key: list(values) for key, values in merged_data.items()}
    return final_data


def __call_techniknews_api(ip: str):
    """
    Calls the TechnikNews IP geolocation API.

    Args:
        ip (str): The IP address to query.

    Returns:
        dict: A dictionary containing IP information from the TechnikNews API,
              or None if the API call fails or returns invalid data.
    """
    answer = requests.get(url=IPGEO_TECHNIKNEWS + ip, timeout=30)

    if answer.status_code == 200:
        answer_json = answer.json()
        if len(answer_json["country"]) > 3:
            return {
                "continent": answer_json["continent"],
                "country": answer_json["country"],
                "city": answer_json["city"],
                "zip": answer_json["zip"],
                "isp": answer_json["isp"],
                "org": answer_json["org"],
                "as": answer_json["as"],
                "lon": answer_json["lon"],
                "lat": answer_json["lat"],
            }

    return None


def __call_ipapi_api(ip: str):
    """
    Calls the ipapi.co API.

    Args:
        ip (str): The IP address to query.

    Returns:
        dict: A dictionary containing IP information from the ipapi.co API,
              or None if the API call fails or returns invalid data.
    """
    answer = requests.get(url=__get_ipapi_url(ip=ip), timeout=30)

    if answer.status_code == 200:
        answer_json = answer.json()
        if len(answer_json["country_name"]) > 3:
            return {
                "country": answer_json["country_name"],
                "in_eu": answer_json["in_eu"],
                "population": answer_json["country_population"],
                "area": answer_json["country_area"],
                "org": answer_json["org"],
                "asn": answer_json["asn"],
                "lon": answer_json["longitude"],
                "lat": answer_json["latitude"],
                "languages": answer_json["languages"],
            }

    return None


def __call_ipwhois_api(ip: str):
    """
    Calls the ipwho.is API.

    Args:
        ip (str): The IP address to query.

    Returns:
        dict: A dictionary containing IP information from the ipwho.is API,
              or None if the API call fails or returns invalid data.
    """
    answer = requests.get(url=IPWHOIS_ENDPOINT + ip, timeout=30)

    if answer.status_code == 200:
        answer_json = answer.json()
        if len(answer_json["country"]) > 3:
            return {
                "region": answer_json["region"],
                "borders": answer_json["borders"],
                "isp_domain": answer_json["connection"]["domain"],
                "flag_emoji": answer_json["flag"]["emoji"],
            }

    return None


def __call_freeipapi_api(ip: str):
    """
    Calls the freeipapi.com API.

    Args:
        ip (str): The IP address to query.

    Returns:
        dict: A dictionary containing IP information from the freeipapi.com API,
              or None if the API call fails or returns invalid data.
    """
    answer = requests.get(url=FREEAPIAPI_ENDPOINT + ip, timeout=30)

    if answer.status_code == 200:
        answer_json = answer.json()
        if len(answer_json["countryName"]) > 3:
            return {
                "tlds": "".join(answer_json["tlds"]),
            }

    return None
