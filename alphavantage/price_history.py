"""
Alpha Vantage API Adapter.

API Documentation
-----------------
https://www.alphavantage.co/documentation/
"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from operator import itemgetter
from json import JSONDecodeError
from urllib.error import HTTPError

import requests
from foil.formatters import format_repr_info
from foil.records import rename_keys

from alphavantage.dates import parse_date, parse_datetime, convert_to_utc
from alphavantage.reference import (
    INTRADAY, DAILY, WEEKLY, MONTHLY, OPEN, HIGH, LOW, CLOSE,
    VOLUME, ADJUSTED_CLOSE, DIVIDEND, SPLIT_COEFFICIENT
)
from alphavantage import web


# output size options
COMPACT = 'compact'
FULL = 'full'

# Period Options
PERIODS = {
    INTRADAY: 'INTRADAY',
    DAILY: 'DAILY',
    WEEKLY: 'WEEKLY',
    MONTHLY: 'MONTHLY',
}

# Timestamp fields
DATE = 'as_of_date'
DATETIME = 'as_of_time'

API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY', '')


def format_interval(interval):
    """Format intraday interval."""

    return f'{interval}min'


RESPONSE_KEY_MAP = {
    DAILY: 'Time Series (Daily)',
    WEEKLY: 'Weekly Time Series',
    MONTHLY: 'Monthly Time Series'
}

ADJUSTED_RESPONSE_KEY_MAP = {
    DAILY: 'Time Series (Daily)',
    WEEKLY: 'Weekly Adjusted Time Series',
    MONTHLY: 'Monthly Adjusted Time Series'
}

INTRADAY_RESPONSE_KEY_MAP = {
    i: 'Time Series ({})'.format(format_interval(i))
    for i in [1, 5, ]
}

FIELD_PARSERS = {
    OPEN: float,
    HIGH: float,
    LOW: float,
    CLOSE: float,
    VOLUME: int,
    ADJUSTED_CLOSE: float,
    DIVIDEND: float,
    SPLIT_COEFFICIENT: float
}


class Results:
    """Container for price history results."""

    def __init__(self, ticker, records, timezone, updated_at, retrieved_at):
        self.ticker = ticker
        self.records = records
        self.timezone = timezone
        self.updated_at = updated_at
        self.retrieved_at = retrieved_at

    def __eq__(self, other):
        return self.ticker == other.ticker

    def __repr__(self):
        return format_repr_info(self, ['ticker'])


class PriceHistory:
    """Price information summary for list of securities."""

    adjusted = False
    RESPONSE_MAP = RESPONSE_KEY_MAP

    time_field = DATE
    FIELDS = (OPEN, HIGH, LOW, CLOSE, VOLUME)

    def __init__(self, period=DAILY, output_size=COMPACT, api_key=API_KEY):
        self.period = period
        self.output_size = output_size
        self.api_key = api_key
        self.field_map = dict(
            zip(build_field_names(self.FIELDS), self.FIELDS)
        )
        self.sort_key = itemgetter(self.time_field)
        self.session = requests.session()

    def request_parameters(self, ticker):
        ts_function = get_time_series_function(self.period, self.adjusted)

        parameters = {
            'function': ts_function,
            'symbol': ticker,
            'apikey': self.api_key,
            'outputsize': self.output_size,
        }

        return parameters

    def get(self, ticker):
        parameters = self.request_parameters(ticker)
        response, retrieved_at = web.get(self.session, parameters)

        return self.get_results(ticker, response, retrieved_at)

    def get_results(self, ticker, response, retrieved_at):
        updated_at, timezone, is_intraday = self.transform_meta_data(response['Meta Data'])
        records = self.transform_records(response[self.data_key])
        records = self.sort_records(self.convert_timezones(records, timezone))

        # remove intraday record in daily series
        if is_intraday:
            records = records[0:-1]

        return Results(ticker, records, timezone,
                       updated_at=updated_at, retrieved_at=retrieved_at)

    def sort_records(self, records):
        """Sort records in ascending time order."""

        return sorted(list(records), key=self.sort_key)

    def transform_records(self, records):
        """Convert record field names, parse values and add time field."""

        for time_string, record in records.items():
            data = self.transform_record(record)
            data[self.time_field] = self.parse_time(time_string)

            yield data

    @property
    def data_key(self):
        return self.RESPONSE_MAP[self.period]

    def parse_time(self, d):
        return parse_date(d)

    def convert_timezones(self, records, timezone):
        for record in records:
            yield record

    def transform_record(self, record):
        return self.parse_record(self.adapt_data(record))

    def adapt_data(self, record):
        """Change data record fields."""

        return rename_keys(record, self.field_map)

    def parse_record(self, record):
        """Parse record field values."""

        return {k: FIELD_PARSERS[k](v) for k, v in record.items()}

    def transform_meta_data(self, response_meta):
        refresh_key = next(
            key for key in response_meta if key.endswith('Last Refreshed')
        )
        tz_key = next(
            key for key in response_meta if key.endswith('Time Zone')
        )
        updated_at, is_intraday = self.parse_refresh_time(
            response_meta[refresh_key]
        )
        timezone = response_meta[tz_key]

        return updated_at, timezone, is_intraday

    def parse_refresh_time(self, dt):
        is_intraday = False

        try:
            updated_at = self.parse_time(dt)
        except ValueError:
            updated_at = self.parse_time(dt[0:10])
            is_intraday = True

        return updated_at, is_intraday


class AdjustedPriceHistory(PriceHistory):
    """Adjusted price history."""

    adjusted = True

    RESPONSE_MAP = ADJUSTED_RESPONSE_KEY_MAP
    FIELDS = (
        OPEN, HIGH, LOW, CLOSE, ADJUSTED_CLOSE, VOLUME,
        DIVIDEND, SPLIT_COEFFICIENT
    )


class IntradayPriceHistory(PriceHistory):
    """Intraday price history."""

    time_field = DATETIME
    RESPONSE_MAP = INTRADAY_RESPONSE_KEY_MAP

    def __init__(self, output_size=COMPACT, api_key=API_KEY, interval=1,
                 utc=True):
        super().__init__(
            period=INTRADAY, output_size=output_size, api_key=api_key
        )
        self.interval = interval
        self.utc = utc

    def request_parameters(self, ticker):
        parameters = super().request_parameters(ticker)
        parameters['interval'] = format_interval(self.interval)

        return parameters

    @property
    def data_key(self):
        return self.RESPONSE_MAP[self.interval]

    def parse_time(self, d):
        return parse_datetime(d)

    def convert_timezones(self, records, timezone):
        if self.utc:
            for record in records:
                dt = convert_to_utc(record[self.time_field], timezone)
                record[self.time_field] = dt

                yield record

    def transform_meta_data(self, response_meta):
        updated_at, timezone, _ = super().transform_meta_data(response_meta)

        if self.utc:
            updated_at = convert_to_utc(updated_at, timezone)

        return updated_at, timezone, None


def get_time_series_function(period, adjusted=False):
    """Get the time-series function string"""

    period_code = PERIODS[period]

    func_str = f'TIME_SERIES_{period_code}'

    if adjusted:
        func_str += '_ADJUSTED'

    return func_str


def build_field_names(fields):
    """Build response field names from sorted field list."""

    for index, field in enumerate(fields, 1):
        field = ' '.join(field.split('_'))

        yield f'{index}. {field.lower()}'


def filter_splits(records):
    """Filter adjusted records for splits."""

    for record in records:
        if record[SPLIT_COEFFICIENT] != 1:
            yield record[DATE], record[SPLIT_COEFFICIENT]


def filter_dividends(records):
    """Filter adjusted records for dividends."""

    for record in records:
        if record[DIVIDEND] != 0:
            yield record[DATE], record[DIVIDEND]


def get_results(cls: PriceHistory, tickers: list, parameters: dict):
    """Return multiple results using threads."""

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_ticker = {
            executor.submit(cls(**parameters).get, ticker): ticker
            for ticker in tickers
        }

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]

            try:
                yield ticker, future.result()
            except (HTTPError, JSONDecodeError, KeyError):
                pass
