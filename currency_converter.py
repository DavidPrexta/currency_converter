#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: David Prexta
# File: currency_converter.py

import argparse 
import sys
from converter import currency_converter
from flask import Flask, request


""" web API application """
app = Flask(__name__)


@app.route('/currency_converter')
def converter():
	""" 
	Check arguments provided in http request
	Converts provided amount in input currency to output currency
	"""
	
	input_currency = request.args.get('input_currency')
	output_currency = request.args.get('output_currency')
	amount = request.args.get('amount')
	
	if not amount or not input_currency:
		return "Please enter input currency code or symbol, and amount you wish to transfer."

	amount_error = False
	try:
		amount = float(amount)
	except:
		amount_error = True
	else:
		if amount <= 0:
			amount_error = True

	if amount_error:
		return "Error, amount must be number bigger than 0"
	else:
		result = currency_converter.convert(input_currency, output_currency, amount)
		return result



if __name__ == "__main__":
	""" 
	CLI application
	Converts required amount in input currency to amount in destination currency
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input_currency', required=True, help='input currency - 3 letters name or currency symbol')
	parser.add_argument('-o', '--output_currency', help='requested/output currency - 3 letters name or currency symbol')
	parser.add_argument('-a', '--amount', required=True, type=float, help='amount which we want to convert - float')
	
	arguments = parser.parse_args()

	if arguments.amount <= 0:
		print("Error, amount must be number bigger than 0")
		sys.exit(1)

	result = currency_converter.convert(arguments.input_currency, arguments.output_currency, arguments.amount)
	print(result)
