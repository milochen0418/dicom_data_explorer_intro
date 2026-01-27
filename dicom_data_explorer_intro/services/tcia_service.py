import requests
import logging

TCIA_BASE_URL = "https://services.cancerimagingarchive.net/services/v2/TCIA/query"


def fetch_collections() -> list[dict]:
    try:
        response = requests.get(
            f"{TCIA_BASE_URL}/getCollectionValues",
            params={"format": "json"},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.exception(f"Error fetching collections: {e}")
        return []


def fetch_modalities(collection: str = "") -> list[dict]:
    try:
        params = {"format": "json"}
        if collection:
            params["Collection"] = collection
        response = requests.get(
            f"{TCIA_BASE_URL}/getModalityValues", params=params, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.exception(f"Error fetching modalities: {e}")
        return []


def fetch_body_parts(collection: str = "") -> list[dict]:
    try:
        params = {"format": "json"}
        if collection:
            params["Collection"] = collection
        response = requests.get(
            f"{TCIA_BASE_URL}/getBodyPartValues", params=params, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.exception(f"Error fetching body parts: {e}")
        return []


def fetch_series(
    collection: str = "", modality: str = "", body_part: str = ""
) -> list[dict]:
    try:
        params = {"format": "json"}
        if collection:
            params["Collection"] = collection
        if modality:
            params["Modality"] = modality
        if body_part:
            params["BodyPartExamined"] = body_part
        response = requests.get(f"{TCIA_BASE_URL}/getSeries", params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.exception(f"Error fetching series: {e}")
        return []