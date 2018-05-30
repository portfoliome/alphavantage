from datetime import datetime
from functools import lru_cache

import pytz

# Date formats
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@lru_cache(8192)
def convert_to_utc(dt: datetime, timezone: str) -> datetime:
    """Convert naive datetime with timezone label to UTC."""

    zone = pytz.timezone(timezone)

    return zone.localize(dt).astimezone(pytz.UTC)


def parse_datetime(d, formatter=DATETIME_FORMAT):
    return datetime.strptime(d, formatter)


def parse_date(d):
    return parse_datetime(d, formatter=DATE_FORMAT).date()
