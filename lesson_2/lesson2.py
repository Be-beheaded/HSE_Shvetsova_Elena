from lesson_2_dzdata import courts, respondents


# Задание 1
def factorial(num: int) -> int:
    res = 1
    while num > 1:
        res *= num
        num -= 1
    return res


def search_max(inp: {int, int, int}) -> int:
    return sorted(inp, reverse=True)[0]


def area(katet1: int, katet2: int):
    return (katet1 * katet2) / 2


# Задание 2
def get_court_header(court):
    header = (f"В {court['court_name']} \n"
              f"Адрес: {court['court_address']} \n")
    print(header)


def get_suitor_header():
    header = ("Истец: Швецова Елена Александровна \n"
              "ИНН 1233982357 ОГРНИП 2184373567812733 \n"
              "Адрес: 123534, г. Москва, ул. Водников, 46 \n")
    print(header)


def get_respondent_header(respondent):
    header = (f"Ответчик: {respondent['short_name']} \n"
              f"ИНН {respondent['inn']} ОГРН {respondent['ogrn']} \n"
              f"Адрес: {respondent['address']} \n \n"
              f"Номер дела {respondent['case_number']} \n")
    print(header)


def main():
    # Задание 1
    print(factorial(6))
    print(search_max({5, 2, 1999}))
    print(area(4, 5))
    # Задание 2
    court_maping = {i['court_code']: i for i in courts}
    for i in respondents:
        try:
            code = i['case_number'][:3]
            court = court_maping[code]
            get_court_header(court)
            get_suitor_header()
            get_respondent_header(i)
        except Exception:
            print("Error")
            continue


if __name__ == "__main__":
    main()
