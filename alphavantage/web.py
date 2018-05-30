from datetime import datetime

import requests

from alphavantage.reference import BASE_URL


def get(session: requests.Session, parameters=None, url=BASE_URL):
    """Request data as JSON."""

    response = session.get(url, params=parameters)
    retrieved_at = datetime.utcnow()

    return response.json(), retrieved_at
