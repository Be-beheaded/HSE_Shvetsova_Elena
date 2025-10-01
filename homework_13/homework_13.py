import datetime
import json
import requests
from bs4 import BeautifulSoup


class ParserCBRF:
    BASE_URL = 'https://www.cbr.ru'

    def __init__(self):
        pass

    def __save_parsed_data_to_json(self, output_path, parsed_data):
        data_to_save = {
            "cbr_key_rate_list": parsed_data
        }
        with open(output_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def __parse_cbr_data(self, soup: BeautifulSoup):
        cells = soup.find(class_='table').find_all('td')
        dates = [d.text for i, d in enumerate(cells) if i % 2 == 0]
        rates = [d.text for i, d in enumerate(cells) if i % 2 != 0]
        return dict(zip(dates, rates))

    def __get_cbr_soup(self):
        date = datetime.date.today()
        parse_date_str = date.strftime('%d.%m.%Y')

        params = ("?UniDbQuery.Posted=True"
                  "&UniDbQuery.From=17.09.2013"
                  f"&UniDbQuery.To={parse_date_str}"
                  )

        data_url = f'{self.BASE_URL}/hd_base/KeyRate/{params}'
        request = requests.get(data_url)
        request.raise_for_status()
        return BeautifulSoup(request.text, 'html.parser')

    def start(self):
        cbr_soup = self.__get_cbr_soup()
        parsed_data = self.__parse_cbr_data(cbr_soup)
        self.__save_parsed_data_to_json('cbr_key_rate.json', parsed_data)


def main():
    parser = ParserCBRF()
    parser.start()


if __name__ == '__main__':
    main()
