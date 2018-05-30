import unittest
from datetime import datetime

import pytz

from alphavantage.dates import convert_to_utc


class TestHelperFunctions(unittest.TestCase):
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
