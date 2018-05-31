import unittest
from datetime import date, datetime

import pytz

from alphavantage.dates import convert_to_utc
from alphavantage.price_history import (
    AdjustedPriceHistory, build_field_names, get_time_series_function, FULL,
    IntradayPriceHistory, PriceHistory, format_interval, Results
)
from tests.fixtures import (
    MOCK_META, MOCK_DAILY_RECORDS, MOCK_DAILY_PRICE_RESPONSE,
    MOCK_ADJUSTED_RECORDS, MOCK_INTRADAY_RESPONSE
)


class TestHelperFunctions(unittest.TestCase):
    def test_build_field_names(self):
        fields = ['alpha', 'beta_gamma']

        expected = ['1. alpha', '2. beta gamma']
        result = list(build_field_names(fields))

        self.assertEqual(expected, result)

    def test_convert_to_utc_winter(self):
        d = datetime(2018, 1, 25, 16, 0, 0)

        expected = datetime(2018, 1, 25, 21, 0, 0, tzinfo=pytz.UTC)
        result = convert_to_utc(d, 'US/Eastern')

        self.assertEqual(expected, result)

    def test_convert_to_utc(self):
        d = datetime(2018, 5, 25, 16, 0, 0)

        expected = datetime(2018, 5, 25, 20, 0, 0, tzinfo=pytz.UTC)
        result = convert_to_utc(d, 'US/Eastern')

        self.assertEqual(expected, result)

    def test_get_time_series_function(self):
        expected = 'TIME_SERIES_MONTHLY'
        result = get_time_series_function('M')

        self.assertEqual(expected, result)

    def test_get_time_series_function_adjusted(self):
        expected = 'TIME_SERIES_DAILY_ADJUSTED'
        result = get_time_series_function('D', adjusted=True)

        self.assertEqual(expected, result)

    def test_format_interval(self):
        expected = '5min'
        result = format_interval(5)

        self.assertEqual(expected, result)


class TestPriceHistory(unittest.TestCase):
    def setUp(self):
        self.ticker = 'MSFT'
        self.timezone = 'US/Eastern'
        self.updated_at = date(2018, 5, 25)
        self.api_key = 'my_fake_key'
        self.price_history = PriceHistory(api_key=self.api_key, output_size=FULL)
        self.transformed_records = [
            {
                'as_of_date': date(2018, 5, 25),
                'open': 98.3000,
                'high': 98.9800,
                'low': 97.8600,
                'close': 98.3600,
                'volume': 18363918
            },
            {
                'as_of_date': date(2018, 5, 24),
                'open': 98.7250,
                'high': 98.9400,
                'low': 96.8100,
                'close': 98.3100,
                'volume': 26649287
            }
        ]

    def test_request_parameters(self):
        expected = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.ticker,
            'apikey': self.api_key,
            'outputsize': FULL
        }
        result = self.price_history.request_parameters(self.ticker)

        self.assertEqual(expected, result)

    def test_transform_records(self):
        expected = self.transformed_records
        result = list(self.price_history.transform_records(MOCK_DAILY_RECORDS))

        self.assertEqual(expected, result)

    def test_sort_records(self):
        expected = self.transformed_records[::-1]
        result = self.price_history.sort_records(self.transformed_records)

        self.assertEqual(expected, result)

    def test_transform_meta_data(self):
        expected = (self.updated_at, self.timezone)
        result = self.price_history.transform_meta_data(MOCK_META)

        self.assertEqual(expected, result)

    def test_get_results(self):
        retrieved_at = datetime(2018, 5, 25, 9, 0, 30)
        expected = Results(ticker=self.ticker,
                           records=self.transformed_records[::-1],
                           retrieved_at=retrieved_at,
                           updated_at=self.updated_at,
                           timezone=self.timezone)
        result = self.price_history.get_results(
            self.ticker, MOCK_DAILY_PRICE_RESPONSE, retrieved_at
        )

        self.assertEqual(expected.retrieved_at, result.retrieved_at)
        self.assertEqual(expected.updated_at, result.updated_at)
        self.assertEqual(expected.records, result.records)


class TestAdjustedPriceHistory(unittest.TestCase):
    def setUp(self):
        self.price_history = AdjustedPriceHistory()
        self.transformed_records = [
            {
                'as_of_date': date(2018, 5, 25),
                'open': 98.3000,
                'high': 98.9800,
                'low': 97.8600,
                'close': 98.3600,
                'adjusted_close': 98.3600,
                'volume': 17942632,
                'dividend_amount': 0,
                'split_coefficient': 1.0
            },
            {
                'as_of_date': date(2018, 5, 24),
                'open': 98.7250,
                'high': 98.9400,
                'low': 96.8100,
                'close': 98.31000,
                'adjusted_close': 98.3100,
                'volume': 26649287,
                'dividend_amount': 0,
                'split_coefficient': 1.0
            },
            {
                'as_of_date': date(2018, 5, 23),
                'open': 96.7100,
                'high': 98.7300,
                'low': 96.3200,
                'close': 98.6600,
                'adjusted_close': 98.6600,
                'volume': 21251222,
                'dividend_amount': 0,
                'split_coefficient': 1.0
            }
        ]

    def test_transform_records(self):
        expected = self.transformed_records
        result = list(self.price_history.transform_records(MOCK_ADJUSTED_RECORDS))

        self.assertEqual(expected, result)


class TestIntraDataPriceHistory(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.ticker = 'MSFT'
        self.timezone = 'US/Eastern'
        self.api_key = 'my_fake_key'
        self.interval = 1
        self.price_history = IntradayPriceHistory(
            api_key=self.api_key, output_size=FULL, interval=self.interval
        )
        self.transformed_records = [
            {'as_of_time': datetime(2018, 5, 30, 20, 0, 0, tzinfo=pytz.UTC),
             'open': 99.0000,
             'high': 99.0500,
             'low': 98.9100,
             'close': 98.9500,
             'volume': 2233252},
            {'as_of_time': datetime(2018, 5, 30, 19, 59, 0, tzinfo=pytz.UTC),
             'open': 99.0350,
             'high': 99.0500,
             'low': 99.0000,
             'close': 99.0000,
             'volume': 156349},
            {'as_of_time': datetime(2018, 5, 30, 19, 58, 0, tzinfo=pytz.UTC),
             'open': 98.9900,
             'high': 99.0600,
             'low': 98.9900,
             'close': 99.0300,
             'volume': 142621}
        ]

    def test_request_parameters(self):
        expected = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.ticker,
            'apikey': self.api_key,
            'outputsize': FULL,
            'interval': f'{self.interval}min'
        }
        result = self.price_history.request_parameters(self.ticker)

        self.assertEqual(expected, result)

    def test_get_results(self):
        retrieved_at = datetime(2018, 5, 30, 9, 0, 30)
        updated_at = datetime(2018, 5, 30, 20, 0, 0, tzinfo=pytz.UTC)
        expected = Results(ticker=self.ticker,
                           records=self.transformed_records[::-1],
                           retrieved_at=retrieved_at,
                           updated_at=updated_at,
                           timezone=self.timezone)
        result = self.price_history.get_results(
            self.ticker, MOCK_INTRADAY_RESPONSE, retrieved_at
        )

        self.assertEqual(expected.retrieved_at, result.retrieved_at)
        self.assertEqual(expected.updated_at, result.updated_at)
        self.assertEqual(expected.records, result.records)
