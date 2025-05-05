import json
import csv
import re


# Задание 1
def read_inn_list(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def load_traders_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)


def save_traders_info_to_csv(inn_list, traders_data, output_csv):
    with open(output_csv, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['INN', 'OGRN', 'ADRESS'])

        for trader in traders_data:
            if trader.get('inn') in inn_list:
                writer.writerow([
                    trader.get('inn', ''),
                    trader.get('ogrn', ''),
                    trader.get('address', '')
                ])


inn_list = read_inn_list('traders.txt')
traders_data = load_traders_data('traders.json')
save_traders_info_to_csv(inn_list, traders_data, 'traders.csv')


# Задание 2

def extract_emails(text):
    pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(pattern, text)


def extract_emails_by_inn(dataset_path, output_path):
    with open(dataset_path, 'r') as f:
        data = json.load(f)

    email_dict = {}

    for msg in data:
        text = msg.get('msg_text', '')
        inn = msg.get('publisher_inn')
        emails = extract_emails(text)
        emails_set = set()
        if emails:
            for email in emails:
                emails_set.add(email)
                email_dict[inn] = list(emails_set)

    with open(output_path, 'w') as f:
        json.dump(email_dict, f)


extract_emails_by_inn('1000_efrsb_messages.json', 'emails.json')
