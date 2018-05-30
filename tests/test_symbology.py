import unittest

from alphavantage.symbology import format_ric_ticker


class TestFormatRicTicker(unittest.TestCase):
    def test_domestic_ticker(self):
        expected = 'AAPL'
        result = format_ric_ticker(expected, 'NAS')

        self.assertEqual(expected, result)

    def test_foreign_ticker(self):
        expected = 'VOD.L'
        result = format_ric_ticker('VOD', 'LON')

        self.assertEqual(expected, result)
