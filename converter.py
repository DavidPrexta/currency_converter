# -*- coding: utf-8 -*-
# Author: David Prexta
# File: converter.py

import requests
import json
import sys
import os
import constants as cons
from collections import OrderedDict

class CurrencyConverter():
	""" Class for currency converter """

	def __init__(self):
		self.currency_table = None
		self.api_endpoint = cons.API_ENDOPINT


	def _init_symbols_table(self):
		""" Load table of currency codes and their symbols from saved file """
		file_path = os.path.dirname(os.path.abspath(__file__))
		file_path = os.path.join(file_path, cons.CURENCY_SYMBOLS_FILE)

		try:
			f = open(file_path)
			self.currency_table = json.loads(f.read(), object_pairs_hook=OrderedDict)
		except IOError:
			print(cons.FILE_IO_ERROR.format(file_path))
		except ValueError:
			print(cons.JSON_ERROR.format(file_path))
		except Exception as e:
			print(e)
		else:
			f.close()	


	def _generate_error_msg(self, msg):
		""" Return output in json that represents error """
		return json.dumps({'error' : msg}, indent=4)


	def _generate_output(self, input_currency, amount, conversion_result):
		""" generate output in json """
		output = {}
		
		output['output'] = conversion_result

		output['input'] = {
			'amount' : round(amount, 2),
			'currency' : input_currency
		}

		return json.dumps(output, indent=4, sort_keys=True)


	def _get_currency_code(self, currency):
		""" 
		Check if currency code is valid or if symbol represents any valid currency
		Returns list of currency codes or empty list
		"""
		if not currency:
			return [code for code in self.currency_table]

		if currency in self.currency_table:
			return [currency]

		return [code for code in self.currency_table if self.currency_table[code] == currency]


	def convert(self, input_currency, output_currency, amount):
		""" Convert amount provided in input currency to output currency """
		
		## Get code for input currency - if input symbol or code is unknown error message is generated ##
		base_code = self._get_currency_code(input_currency)
		if not base_code:
			return self._generate_error_msg(cons.CCODE_ERROR.format(input_currency))
		base_code = base_code[0]

		## Get codes for output currencies - if output symbol or code is unknown error message is generated ##
		dest_codes = self._get_currency_code(output_currency)
		if not dest_codes:
			return self._generate_error_msg(cons.CCODE_ERROR.format(output_currency))

		## if input and output currencies are same, script will return same amount ##
		if base_code in dest_codes and len(dest_codes) == 1:
			return self._generate_output(base_code, amount, {base_code : amount})

		## try to get rates form fixer.io api for required currencies ##
		payload = {'base':  base_code, 'symbols': ','.join(dest_codes)}
		try:
			r = requests.get(self.api_endpoint , params = payload)
			result = r.json()
		except requests.exceptions.ConnectionError:
			return self._generate_error_msg(cons.CON_ERROR)
		except requests.exceptions.Timeout:
			return self._generate_error_msg(cons.TIMEOUT_ERROR)
		except:
			return self._generate_error_msg(cons.UNKNOWN_ERROR)

		if not r.status_code == 200:
			return self._generate_error_msg(result['error'])

		## calculate amount in destination curencies based on acquired rates ##
		conversion_result = {}
		for code in result['rates']:
			rate = result['rates'][code]
			conversion_result[code] = round(rate * amount, 2)

		## generate an return result in json ##
		return self._generate_output(base_code, amount, conversion_result)


""" Creates currency converter and initialize table of symbols """
currency_converter = CurrencyConverter()
currency_converter._init_symbols_table()

if not currency_converter.currency_table:
	sys.exit(1)