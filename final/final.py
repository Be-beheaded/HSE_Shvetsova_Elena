import time
import json
from json import JSONDecodeError

import requests
from bs4 import BeautifulSoup
import traceback
from pathlib import Path


class ParserZakupki:
    # ВНИМАНИЕ сайт Госзакупок не работает со включенным ВПН
    BASE_URL = 'https://zakupki.gov.ru'
    HEADERS = {
        'Host': 'zakupki.gov.ru',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Cookie': 'doNotAdviseToChangeLocationWhenIosReject=true; _ym_uid=1760111657141512250; _ym_d=1760111657; session-cookie=186e6c1444fe7242bbacfc6d4c95548f7c1a1b8766da3b715ea1dd77bb00fda2f92596c64b8fd7cc70d37c05e5da578c; _ym_isad=2; _ym_visorc=b',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }

    def __init__(self):
        pass

    def _save_parsed_data_to_json(self, filename: str, parsed_data: dict):
        project_root = Path(__file__).resolve().parent

        parsed_data_dir = project_root / "parsed_data"
        parsed_data_dir.mkdir(exist_ok=True)

        output_path = parsed_data_dir / filename

        data = {}
        if output_path.exists():
            try:
                with output_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    data.update(parsed_data)
            except JSONDecodeError:
                data = parsed_data
        else:
            data = parsed_data

        with output_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _parse_cbr_data(self, soup: BeautifulSoup):
        data_dict = {}
        data = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')

        for item in data:
            contract_num = item.find_all(class_='registry-entry__header-mid__number')[0].text.replace("№", "").strip()
            status = item.find_all(class_='registry-entry__header-mid__title')[0].text.strip()
            data_dict[contract_num] = status
        return data_dict

    def _get_cbr_soup(self, page_number):
        params = (f"results.html?searchString=7750005919&pageNumber={page_number}&recordsPerPage=_50"
                  )
        data_url = f'{self.BASE_URL}/epz/order/extendedsearch/{params}'

        for _ in range(5):
            try:
                request = requests.get(data_url, headers=self.HEADERS)
                request.raise_for_status()
                soup = BeautifulSoup(request.text, 'html.parser')
                return soup
            except requests.exceptions.ReadTimeout:
                print('Timeout exceeded')
                time.sleep(1)
                continue
            except requests.exceptions.HTTPError:
                print('HTTPError on page:', page_number)
                time.sleep(1)
                continue
            except Exception as exc:
                print(traceback.format_exception(exc))
                break
        return None

    def start(self):
        print('Начался парсинг сайта, ожидайте')
        page_number = 1
        while True:
            print(f'Парсинг страницы {page_number}')
            cbr_soup = self._get_cbr_soup(page_number)
            parsed_data = self._parse_cbr_data(cbr_soup)
            if not parsed_data:
                break
            self._save_parsed_data_to_json('data.json', parsed_data)
            page_number += 1
        print('Данные сохранены')



class ZakupkiGov:
    data = {}

    def __init__(self):
        project_root = Path(__file__).resolve().parent
        parsed_data_dir = project_root / "parsed_data"

        output_path = parsed_data_dir / "data.json"
        if output_path.exists():
            with output_path.open("r", encoding="utf-8") as f:
                self.data = json.load(f)

    def find_status_by_number(self, number):
        if number in self.data:
            print(f'Статус закупки {number} - {self.data[number]}')
        else:
            print('Номер договора не найден')

    def find_numbers_by_status(self, status):
        keys_found = [key for key, value in self.data.items() if value == status]
        if keys_found:
            print(f'Все закупки со статусом "{status}":')
            for key in keys_found:
                print(f'- {key}')
        else:
            print("Закупки с таким статусом не найдены")


def main():
    parser = ParserZakupki()
    parser.start()

    zakupki = ZakupkiGov()
    zakupki.find_status_by_number("32515021370")
    zakupki.find_numbers_by_status("Определение поставщика завершено")


if __name__ == '__main__':
    main()
