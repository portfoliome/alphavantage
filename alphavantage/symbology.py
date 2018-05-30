"""
Mapping for Factset exchange codes to Reuter's RICs.

-- Yahoo Reference with exchange name and RIC suffixes
https://help.yahoo.com/kb/SLN2310.html

-- Reuters company lookup
https://www.reuters.com/finance/stocks/lookup
"""


# Factset exchange code to RIC suffix
FACTSET_EXCHANGE_TO_SUFFIX_MAP = {
    'AMS': 'AS',
    'ASX': 'AX',
    'ATH': 'AT',
    'BAR': 'BC',
    'BER': 'BE',
    'BKK': 'BK',
    'BOM': 'BO',
    'BRU': 'BR',
    'BSP': 'SA',
    'BUE': 'BA',
    'CAI': 'CA',
    'CAR': 'CR',
    'CSE': 'CO',
    'DSMD': 'QA',
    'DUB': 'IR',
    'DUS': 'DU',
    'ETR': 'DE',
    'FRA': 'F',
    'HAM': 'HM',
    'HEL': 'HE',
    'HKG': 'HK',
    'ICE': 'IC',
    'IST': 'IS',
    'JKT': 'JK',
    'JSE': 'JO',
    'KLS': 'KL',
    'KRX': 'KS',
    'LIS': 'LS',
    'LIT': 'VS',
    'LON': 'L',
    'MAD': 'MA',
    'MEX': 'MX',
    'MIC': 'ME',
    'MIL': 'MI',
    'MUN': 'MU',
    'NAS': None,
    'NSE': 'NS',
    'NYS': None,
    'NZE': 'NZ',
    'OME': 'ST',
    'OSL': 'OL',
    'OTC': None,
    'PAR': 'PA',
    'PRA': 'PR',
    'RIS': 'RG',
    'SAU': 'SAU',
    'SES': 'SI',
    'SGO': 'SN',
    'SHE': 'SZ',
    'SHG': 'SS',
    'STU': 'SG',
    'SWX': 'SW',
    'TAE': 'TA',
    'TAI': 'TW',
    'TAL': 'TL',
    'TKS': 'T',
    'TSE': 'TO',
    'TSX': 'V',
    'WBO': 'VI'
}


def format_ric_ticker(ticker, exchange_code):
    """Format RIC ticker from Factset exchange code."""

    suffix = FACTSET_EXCHANGE_TO_SUFFIX_MAP[exchange_code]

    if suffix:
        ticker = f'{ticker}.{suffix}'

    return ticker
