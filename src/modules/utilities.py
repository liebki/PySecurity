"""Simple module to provide pre-configured stuff, currently the random header def for requests."""

# pylint: disable=C0301

import random

user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/122.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15) Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.2210.133",
]

headers = {"Accept-Language": "en-US,en;q=0.9"}


def get_headers():
    """
    Get a useable header with random user agent.

    Returns:
        dict: A pre-configured header with random user agent from list.
    """
    headers["User-Agent"] = random.choice(user_agents)
    return headers


def get_random_ua():
    return random.choice(user_agents)
