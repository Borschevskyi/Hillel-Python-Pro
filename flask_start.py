from flask import Flask, request

from utils import get_currency_exchange_rate, get_pb_exchange_rate
from db_practice import get_customers, unwrapper

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p><b>Hello, World!</b></p>"


@app.route("/rates", methods=["GET"])
def get_rates():
    currency_a = request.args.get("currency_a", default="USD")
    currency_b = request.args.get("currency_b", default="UAH")
    result = get_currency_exchange_rate(currency_a, currency_b)
    return result


@app.route("/rates_pb", methods=["GET"])
def get_pb_rates():
    convert_currency = request.args.get("convert_currency", default="USD")
    bank = request.args.get("bank", default="NB")
    rate_date = request.args.get("rate_date", default="06.06.2022")
    result = get_pb_exchange_rate(convert_currency, bank, rate_date)
    return result


@app.route('/customers')
def show_customers():
    """Функция для вывода результата выполнения запроса"""
    state_name = request.args.get('state_name', default = None)
    city_name = request.args.get('city_name', default = None)
    customers = get_customers(state_name, city_name)
    customer_list = ''
    for customer in customers:
        customer_list += f"{customer[0]}\n"

    return customer_list
