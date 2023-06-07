import requests

from dateutil import parser
from datetime import datetime
from urllib import parse


def get_currency_iso_code(currency: str) -> int:
    """
    Функція повертає ISO код валюти
    :param currency: назва валюти
    :return: код валюти
    """
    currency_dict = {
        "UAH": 980,
        "USD": 840,
        "EUR": 978,
        "GBP": 826,
        "AZN": 944,
        "CAD": 124,
        "PLN": 985,
    }
    try:
        return currency_dict[currency]
    except:
        raise KeyError("Currency not found! Update currencies information")


def get_currency_exchange_rate(currency_a: str, currency_b: str) -> str:
    currency_code_a = get_currency_iso_code(currency_a)
    currency_code_b = get_currency_iso_code(currency_b)

    response = requests.get("https://api.monobank.ua/bank/currency")
    json = response.json()

    if response.status_code == 200:
        for i in range(len(json)):
            if (
                json[i].get("currencyCodeA") == currency_code_a
                and json[i].get("currencyCodeB") == currency_code_b
            ):
                date = datetime.fromtimestamp(int(json[i].get("date"))).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                rate_buy = json[i].get("rateBuy")
                rate_sell = json[i].get("rateSell")
                return f"exchange rate {currency_a} to {currency_b} for {date}: \n rate buy - {rate_buy} \n rate sell - {rate_sell}"
            return f"Not found: exchange rate {currency_a} to {currency_b}"
    else:
        return f"Api error {response.status_code}: {json.get('errorDescription')}"


# print(get_currency_exchange_rate('USD', 'UAH'))


def get_pb_exchange_rate(convert_currency: str, bank: str, rate_date: str) -> str:
    def validate_date(rate_date: str) -> str:  # added validation function for date
        try:
            date_object = parser.parse(rate_date)
            output_date = date_object.strftime("%d.%m.%Y")
            return output_date
        except:
            return f"{rate_date} is not a valid date"

    def validate_bank(bank: str) -> str:  # added validation function for banks
        nbu_banks = ["nbu", "nationalbank", "NationalBank", "NB"]
        pb_banks = ["pb", "PB", "privatbank", "PrivatBank"]

        if bank in nbu_banks:
            return "NB"
        elif bank in pb_banks:
            return "PB"
        else:
            return f"Rates for {bank} are not supported"  # Error message for unsupported bank

    bank = validate_bank(bank)
    rate_date = validate_date(rate_date)

    params = {
        "json": "",
        "date": rate_date,
    }

    query = parse.urlencode(params)
    api_url = "https://api.privatbank.ua/p24api/exchange_rates?"
    response = requests.get(api_url + query)
    json = response.json()

    if response.status_code == 200:
        rates = json["exchangeRate"]
        for rate in rates:
            if rate["currency"] == convert_currency:
                if bank == "NB":
                    try:
                        sale_rate = rate["saleRateNB"]
                        purchase_rate = rate["purchaseRateNB"]
                        return f"Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}"
                    except:
                        return f"There is no exchange rate NBU for {convert_currency}"
                elif bank == "PB":
                    try:
                        sale_rate = rate["saleRate"]
                        purchase_rate = rate["purchaseRate"]
                        return f"Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}"
                    except:
                        return f"There is no exchange rate PrivatBank for {convert_currency}"
                else:
                    return f"{bank} for {convert_currency}"
    else:
        return f"Error {response.status_code}"


result_PB1 = get_pb_exchange_rate("USD", "privatbank", "2023-05-31")
result_PB2 = get_pb_exchange_rate("EUR", "pb", "31-05-2023")
result_PB3 = get_pb_exchange_rate("GBP", "PrivatBank", "31.05.2023")
result_PB4 = get_pb_exchange_rate("USD", "PB", "01.01.2010")

result_NB1 = get_pb_exchange_rate("USD", "nationalbank", "2023-05-31")
result_NB2 = get_pb_exchange_rate("EUR", "nbu", "31-05-2023")
result_NB3 = get_pb_exchange_rate("AZN", "NationalBank", "31.05.2023")
result_NB4 = get_pb_exchange_rate("USD", "NB", "01.01.2010")

result_AlphaBank = get_pb_exchange_rate("USD", "AlphaBank", "5.31.2023")
result_SomeUnsupportedBank = get_pb_exchange_rate("EUR", "SomeUnsupportedBank", "5.31.2023")

print(result_PB1)
print(result_PB2)
print(result_PB3)
print(result_PB4)

print(result_NB1)
print(result_NB2)
print(result_NB3)
print(result_NB4)

print(result_AlphaBank)
print(result_SomeUnsupportedBank)
