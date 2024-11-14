from dotenv import load_dotenv
import os, logging

from flask import Flask, render_template, request
import requests

load_dotenv()
app = Flask(__name__)

API_URL = 'https://api.freecurrencyapi.com/v1/latest'
API_KEY = os.getenv('FREE_CURRENCY_API_KEY')

logging.info(f"The API key = {API_KEY}")

CURRENCIES = [
    'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY',
    'HKD', 'NZD', 'SEK', 'KRW', 'SGD', 'NOK', 'MXN', 'INR',
    'RUB', 'ZAR', 'TRY', 'BRL', 'TWD', 'DKK', 'PLN', 'THB',
    'IDR', 'HUF', 'CZK', 'ILS', 'CLP', 'PHP', 'AED', 'COP',
    'SAR', 'MYR', 'RON'
]

def validate_amount(amount_str):
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None, "Please enter a positive amount."
        else:
            return amount, None
    except ValueError:
        return None, "Invalid amount entered."

def calculate_conversion(amount, rate):
    return amount * rate

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    selected_from = 'EUR'  # Default selection
    selected_to = 'USD'    # Default selection
    amount = 1.0             # Default amount

    if request.method == 'POST':
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        amount_str = request.form.get('amount', '1.0')

        if from_currency:
            selected_from = from_currency
        if to_currency:
            selected_to = to_currency

        # Validate the amount
        amount, validation_error = validate_amount(amount_str)
        if validation_error:
            error = validation_error

        if selected_from == selected_to:
            error = "Please select two different currencies."

        if not error:
            params = {
                'apikey': API_KEY,
                'base_currency': selected_from,
                'currencies': selected_to
            }
            try:
                response = requests.get(API_URL, params=params)
                response.raise_for_status()
                data = response.json()
                if 'data' in data and selected_to in data['data']:
                    rate = data['data'][selected_to]
                    converted_amount = calculate_conversion(amount, rate)
                    result = f"{amount} {selected_from} = {converted_amount:.2f} {selected_to}"
                else:
                    error = "Error fetching data. Please try again."
            except requests.exceptions.RequestException as e:
                error = f"An error occurred: {str(e)}"

    return render_template(
        'index.html',
        currencies=CURRENCIES,
        result=result,
        error=error,
        selected_from=selected_from,
        selected_to=selected_to,
        amount=amount 
    )

if __name__ == '__main__':
    if not API_KEY:
        raise ValueError("No API key found. Please set the FREE_CURRENCY_API_KEY environment variable.")
    # Retrieve the port from the environment variable, default to 5000
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)