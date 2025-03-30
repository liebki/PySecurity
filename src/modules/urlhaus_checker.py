"""
URLhaus Checker Module

This module provides functionality to check URLs against the URLhaus database,
which contains information about malicious URLs. It downloads and maintains
local copies of the URLhaus database files and provides methods to check if
a given URL exists in the database.

The module handles:
- Downloading and maintaining local copies of URLhaus data
- Checking URL existence in the database
- Managing file freshness and cleanup
"""

import os
import json
import datetime
from datetime import datetime, timezone
import requests

DOWNLOAD_URLS = {
    "recent-elements.json": "https://urlhaus.abuse.ch/downloads/json_recent/",
    "active-elements.json": "https://urlhaus.abuse.ch/downloads/json_online/",
}

MILLISECONDS_DAY = 86_400_000


def __download_json():
    """
    Downloads the latest JSON data from URLhaus for both recent and active elements.
    Saves the data with timestamp-prefixed filenames and cleans up old files.
    """
    for key, value in DOWNLOAD_URLS.items():
        answer = requests.get(url=value, timeout=120)
        answer_json = answer.json()

        with open(
            file=f"{__get_timestamp()}-" + key, mode="w", encoding="utf-8"
        ) as filewriter:
            json.dump(answer_json, filewriter, ensure_ascii=False, indent=4)

    __delete_old_files()


def __files_check() -> bool:
    """
    Performs two checks on the local URLhaus database files:
    1. Verifies that all required files are present
    2. Verifies that all files are less than a day old

    Returns:
        bool: True if all files exist and are fresh, False otherwise
    """
    files_present = True
    for key, _ in DOWNLOAD_URLS.items():
        matching_files = [f for f in os.listdir(".") if f.endswith(key)]
        if not matching_files:
            files_present = False
            break

    files_fresh = True
    for key, _ in DOWNLOAD_URLS.items():
        matching_files = [f for f in os.listdir(".") if f.endswith(key)]
        if matching_files:
            latest_file = max(matching_files)
            try:
                timestamp_of_file = float(latest_file.split("-")[0])
                if __day_elapsed(file_timestamp=timestamp_of_file):
                    files_fresh = False
                    break
            except (ValueError, IndexError):
                files_fresh = False
                break

    return files_present and files_fresh


def __delete_old_files():
    """
    Removes all but the most recent file for each type of URLhaus data.
    This helps maintain a clean directory with only the latest data files.
    """
    for key, _ in DOWNLOAD_URLS.items():
        matching_files = [f for f in os.listdir(".") if f.endswith(key)]
        if len(matching_files) > 1:
            # Sort files by timestamp (newest first)
            sorted_files = sorted(matching_files, reverse=True)
            # Keep the newest file, delete the rest
            for old_file in sorted_files[1:]:
                try:
                    os.remove(old_file)
                except OSError:
                    continue


def check_existence(check_input: str):
    """
    Checks if a given URL exists in the URLhaus database.

    Args:
        input (str): The URL to check for existence in the database

    Returns:
        list: A list of occurrences, where each occurrence is a list containing:
            [dateadded, url, threat, urlhaus_link]
    """
    if not __files_check():
        __download_json()

    occurences = []
    for key, _ in DOWNLOAD_URLS.items():
        matching_files = [f for f in os.listdir(".") if f.endswith(key)]
        if matching_files:
            latest_file = max(matching_files)
            try:
                with open(file=latest_file, mode="r", encoding="utf-8") as filereader:
                    read_file = json.loads(filereader.read())

                    for _, abuse_data in read_file.items():
                        for element_data in abuse_data:
                            if (
                                element_data["url"]
                                and check_input in element_data["url"]
                            ):
                                el = [
                                    element_data["dateadded"],
                                    element_data["url"],
                                    element_data["threat"],
                                    element_data["urlhaus_link"],
                                ]
                                occurences.append(el)
            except (ValueError, IndexError, OSError):
                continue

    return occurences


def __get_timestamp() -> float:
    """
    Generates a current UTC timestamp in milliseconds.

    Returns:
        float: Current UTC timestamp in milliseconds
    """
    return datetime.now(timezone.utc).timestamp() * 1000


def __day_elapsed(file_timestamp: float) -> bool:
    """
    Checks if a given timestamp is older than one day.

    Args:
        file_timestamp (float): The timestamp to check in milliseconds

    Returns:
        bool: True if the timestamp is older than one day, False otherwise
    """
    difference_ms = __get_timestamp() - file_timestamp
    difference_days = difference_ms / MILLISECONDS_DAY

    return difference_days >= 1
