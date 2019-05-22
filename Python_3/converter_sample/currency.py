from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(date))  # Использовать переданный requests

    soup = BeautifulSoup(response.content, 'xml')
    if cur_from != 'RUR':
        ru_sum = amount * Decimal(str(soup.find('CharCode', text=cur_from).find_next_sibling('Value').string).replace(',', '.'))
        ru_sum = ru_sum / Decimal(str(soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string).replace(',', '.'))
    else:
        ru_sum = amount

    if cur_to != 'RUR':
        out_sum = ru_sum / Decimal(str(soup.find('CharCode', text=cur_to).find_next_sibling('Value').string).replace(',', '.'))
        out_sum = out_sum * Decimal(str(soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string).replace(',', '.'))
    else:
        out_sum = ru_sum
    result = out_sum.quantize(Decimal('.0001'))

    return result