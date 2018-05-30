
# daily price response
MOCK_META = {
    "1. Information": "Daily Prices (open, high, low, close) and Volumes",
    "2. Symbol": "MSFT",
    "3. Last Refreshed": "2018-05-25",
    "4. Output Size": "Full size",
    "5. Time Zone": "US/Eastern"
}

MOCK_DAILY_RECORDS = {
    "2018-05-25": {
        "1. open": "98.3000",
        "2. high": "98.9800",
        "3. low": "97.8600",
        "4. close": "98.3600",
        "5. volume": "18363918"
    },
    "2018-05-24": {
        "1. open": "98.7250",
        "2. high": "98.9400",
        "3. low": "96.8100",
        "4. close": "98.3100",
        "5. volume": "26649287"
    }
}

MOCK_DAILY_PRICE_RESPONSE = {
    "Meta Data": MOCK_META,
    "Time Series (Daily)": MOCK_DAILY_RECORDS
}


# daily adjusted price response
MOCK_ADJUSTED_META = {
    "1. Information": "Daily Time Series with Splits and Dividend Events",
    "2. Symbol": "MSFT",
    "3. Last Refreshed": "2018-05-25",
    "4. Output Size": "Full size",
    "5. Time Zone": "US/Eastern"
}

MOCK_ADJUSTED_RECORDS = {
    "2018-05-25": {
        "1. open": "98.3000",
        "2. high": "98.9800",
        "3. low": "97.8600",
        "4. close": "98.3600",
        "5. adjusted close": "98.3600",
        "6. volume": "17942632",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0000"
    },
    "2018-05-24": {
        "1. open": "98.7250",
        "2. high": "98.9400",
        "3. low": "96.8100",
        "4. close": "98.3100",
        "5. adjusted close": "98.3100",
        "6. volume": "26649287",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0000"
    },
    "2018-05-23": {
        "1. open": "96.7100",
        "2. high": "98.7300",
        "3. low": "96.3200",
        "4. close": "98.6600",
        "5. adjusted close": "98.6600",
        "6. volume": "21251222",
        "7. dividend amount": "0.0000",
        "8. split coefficient": "1.0000"
    }
}

MOCK_ADJUSTED_PRICE_RESPONSE = {
    "Meta Data": MOCK_ADJUSTED_META,
    "Time Series (Daily)": MOCK_ADJUSTED_RECORDS
}


# intraday price response
MOCK_META_INTRADAY = {
    "1. Information": "Intraday (1min) prices and volumes",
    "2. Symbol": "MSFT",
    "3. Last Refreshed": "2018-05-30 16:00:00",
    "4. Interval": "1min",
    "5. Output Size": "Compact",
    "6. Time Zone": "US/Eastern"
}

MOCK_INTRADAY_RECORDS = {
    "2018-05-30 16:00:00": {
        "1. open": "99.0000",
        "2. high": "99.0500",
        "3. low": "98.9100",
        "4. close": "98.9500",
        "5. volume": "2233252"
    },
    "2018-05-30 15:59:00": {
        "1. open": "99.0350",
        "2. high": "99.0500",
        "3. low": "99.0000",
        "4. close": "99.0000",
        "5. volume": "156349"
    },
    "2018-05-30 15:58:00": {
        "1. open": "98.9900",
        "2. high": "99.0600",
        "3. low": "98.9900",
        "4. close": "99.0300",
        "5. volume": "142621"
    }
}

MOCK_INTRADAY_RESPONSE = {
    "Meta Data": MOCK_META_INTRADAY,
    "Time Series (1min)": MOCK_INTRADAY_RECORDS
}
