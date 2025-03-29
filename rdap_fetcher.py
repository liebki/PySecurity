"""Module for fetching domain registration and contact information using the RDAP protocol."""

import requests

IANA_ENDPOINT = "https://rdap.iana.org/domain/"
REGISTAR_SUFFIX = "domain/"


def get_registars_rdap_endpoint(tld: str):
    """Get the RDAP endpoint URL for a given top-level domain.
    
    Args:
        tld (str): Top-level domain (e.g., 'com', 'org')
        
    Returns:
        str: RDAP endpoint URL for the given TLD
    """
    url = IANA_ENDPOINT + tld
    answer = requests.get(url=url, timeout=120)

    if answer.status_code == 200:
        answer_json = answer.json()
        if answer_json["links"]:
            for registar_link in answer_json["links"]:
                if ("alternate" in registar_link["rel"]) and (registar_link["href"]):
                    return registar_link["href"]

    else:
        return None


def get_domain_contact_informations(domain: str, tld: str):
    """Fetch domain contact information and registration events using RDAP.
    
    Args:
        domain (str): Domain name without TLD (e.g., 'example')
        tld (str): Top-level domain (e.g., 'com')
        
    Returns:
        dict: Dictionary containing contact info (name, tel, mail) and domain events,
              or None if request fails
    """
    registar_endpoint = get_registars_rdap_endpoint(tld=tld)
    url = registar_endpoint + REGISTAR_SUFFIX + domain

    answer = requests.get(url=url, timeout=120)
    if answer.status_code == 200:
        json_answer = answer.json()

        data = {}
        if json_answer["entities"]:
            for entitiy1 in json_answer["entities"]:

                if entitiy1["vcardArray"]:
                    name = entitiy1["vcardArray"][1][1][3]
                    data["name"] = name

                if entitiy1["entities"]:
                    for entitiy2 in entitiy1["entities"]:
                        if entitiy2["vcardArray"]:
                            velements = entitiy2["vcardArray"][1]
                            tel = velements[2][3]
                            mail = velements[3][3]

                            data["tel"] = tel
                            data["mail"] = mail

        events = {}
        if json_answer["events"]:
            for event in json_answer["events"]:
                action = event["eventAction"]
                date = event["eventDate"]

                events[date] = action

        data["events"] = events
        return data

    return None
