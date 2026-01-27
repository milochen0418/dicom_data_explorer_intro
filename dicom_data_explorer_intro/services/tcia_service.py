import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TCIA_BASE_URL = "https://services.cancerimagingarchive.net/services/v2/TCIA/query"

logger = logging.getLogger(__name__)

_RETRY = Retry(
    total=3,
    connect=3,
    read=3,
    backoff_factor=0.5,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
    raise_on_status=False,
)
_SESSION = requests.Session()
_SESSION.mount("https://", HTTPAdapter(max_retries=_RETRY))
_SESSION.mount("http://", HTTPAdapter(max_retries=_RETRY))


def _get_json(endpoint: str, params: dict, timeout: tuple[float, float]) -> list[dict]:
    response = _SESSION.get(endpoint, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_collections() -> list[dict]:
    try:
        return _get_json(
            f"{TCIA_BASE_URL}/getCollectionValues",
            params={"format": "json"},
            timeout=(5, 20),
        )
    except Exception as e:
        logger.warning("Error fetching collections: %s", e)
        return []


def fetch_modalities(collection: str = "") -> list[dict]:
    try:
        params = {"format": "json"}
        if collection:
            params["Collection"] = collection
        return _get_json(
            f"{TCIA_BASE_URL}/getModalityValues",
            params=params,
            timeout=(5, 20),
        )
    except Exception as e:
        logger.warning("Error fetching modalities: %s", e)
        return []


def fetch_body_parts(collection: str = "") -> list[dict]:
    try:
        params = {"format": "json"}
        if collection:
            params["Collection"] = collection
        return _get_json(
            f"{TCIA_BASE_URL}/getBodyPartValues",
            params=params,
            timeout=(5, 20),
        )
    except Exception as e:
        logger.warning("Error fetching body parts: %s", e)
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
        return _get_json(
            f"{TCIA_BASE_URL}/getSeries",
            params=params,
            timeout=(5, 30),
        )
    except Exception as e:
        logger.warning("Error fetching series: %s", e)
        return []