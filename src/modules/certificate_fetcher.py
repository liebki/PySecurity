"""Module for fetching SSL certificate data from crt.sh certificate transparency logs."""

import requests

BASE_ENDPOINT_PRE = "https://crt.sh/json?q="
BASE_ENDPOINT_SUF = "&exclude=expired"


def get_certificate_data(name: str):
    """Fetch SSL certificate data for a given domain name from crt.sh.

    Args:
        name (str): Domain name to query (e.g., 'example.com')

    Returns:
        dict: JSON response containing certificate details or None if request fails
    """
    endpoint = BASE_ENDPOINT_PRE + name + BASE_ENDPOINT_SUF
    answer = requests.get(url=endpoint, timeout=300)

    if answer.status_code == 200:
        return answer.json()

    return None
