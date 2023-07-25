import requests
import argparse
from datetime import datetime


def format_date(date):
    date_string = datetime.strptime(date, "%Y-%m-%d")
    new_date_string = date_string.strftime("%d/%m/%Y")
    return new_date_string


def get_currency_rates(code, date):
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req=" \
          f"{format_date(date)}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content.decode('windows-1251')
        lines = data.split("<Valute ID=")
        for line in lines[1:]:
            code_start = line.find("<CharCode>") + len("<CharCode>")
            code_end = line.find("</CharCode>")
            currency_code = line[code_start:code_end]

            if currency_code == code:
                name_start = line.find("<Name>") + len("<Name>")
                name_end = line.find("</Name>")
                currency_name = line[name_start:name_end]
                value_start = line.find("<Value>") + len("<Value>")
                value_end = line.find("</Value>")
                currency_value = float(line[value_start:value_end]
                                       .replace(",", "."))
                return currency_name, currency_value
    return None, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    currency_name, currency_value \
        = get_currency_rates(args.code, args.date)

    if currency_name and currency_value:
        print(f"{args.code} ({currency_name}): {currency_value}")
    else:
        print("Unable to retrieve currency rates for the specified date.")
