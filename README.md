# Currency converter

Currency converter is simple application that converts input amount from one currency to another.

Exchange rates are obtained by Fixer.io API (http://fixer.io/). This API provides rates published daily by European Central Bank. Currently available currencies that can be used for conversion are listed here: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html

## Requirements
 - Requests:  pip install requests
 - Flask framework: pip install Flask

## CLI application
To run program from command line use script currency_converter.py with input parameters.

Input parameters:
 - amount - amount which we want to convert - float
 - input_currency - input currency - 3 letters name or currency symbol
 - output_currency - requested/output currency - 3 letters name or currency symbol

## WEB API 
To run API on local network use following commands:
 - export FLASK_APP=currency_converter.py
 - flask run
    
This will start API on localhost on port 5000. Parameters for API are same as for CLI application. API is also available here: http://davidprexta.pythonanywhere.com/currency_converter

Example call: http://davidprexta.pythonanywhere.com/currency_converter?amount=1050&input_currency=CZK&output_currency=EUR

## OUTPUT
Aplication returns output in json. 
```
{
    "input": { 
        "amount": <float>,
        "currency": <3 letter currency code>
    }
    "output": {
        <3 letter currency code>: <float>
    }
}
```
In case of any application error, output is json with following structure.
```
{
    "error" : <Error message>
}
```

## Currency symbols

Application accepts currency symbol as input, which is then transformed to currency code. However some currencies have same symbols e.g. symbol for USD and CAD is $. Therefore symbol can't be used as unique key. Application's reaction to symbol is different for input and output currency:
 - symbol in input_currency - if more than one currency is valid for input symbol, application will use first found currency
 - symbol in output_currency -  if more than one currency is valid for output symbol, application will convert input amount to all currencies than match this symbol
