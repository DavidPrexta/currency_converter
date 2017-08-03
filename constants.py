# Author: David Prexta
# File: constants.py

""" Endpoint for API that returns exchange rates """
API_ENDOPINT = 'http://api.fixer.io/latest'

""" File with available currency codes and their symbols """
CURENCY_SYMBOLS_FILE = 'currencies_symbols.json'

""" Error messages """
FILE_IO_ERROR = 'Cant open and read file: {0}'
JSON_ERROR = 'Cant transfer content from file {0} to JSON format'
CCODE_ERROR = 'Error, unknown currency code or symbol: {0}'
CON_ERROR = 'Error, cant connect to fixer.io API for exchange rates'
TIMEOUT_ERROR = 'Error, request to fixer.io API timed out'
UNKNOWN_ERROR = 'Sorry, unknown error ocured'
MISSING_PARAM = 'Please enter input currency code or symbol, and amount you wish to transfer.'
AMOUNT_ERROR = 'Error, amount must be number bigger than 0'
