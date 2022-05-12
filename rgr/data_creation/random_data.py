import random as rm

import requests
from bs4 import BeautifulSoup


def get_name(count=10):
    response = requests.get(
        f"https://randomus.ru/name?type=0&sex=10&count={count}")
    data = BeautifulSoup(response.content, "html.parser")
    parse_data = data.find_all('div', attrs={'class': 'tags copy_button'})
    student_name = []
    for name in parse_data:
        student_name.append(name.text.strip())
    return student_name


def get_city():
    url = 'https://parseapi.back4app.com/classes/City?limit=1200&order=name&keys=name'
    headers = {
        'X-Parse-Application-Id': 'VaVKTbpKMiCYzsF4WjxWhVIlpXBIm2Axn4ugunjl',
        'X-Parse-Master-Key': 's2nVfQsgEDdl3bDY5patrAXpjwZlcQa5rdfuSeYl'
    }
    response = requests.get(url, headers=headers)
    datas = response.json()
    d = datas.get('results')
    city_list = []
    for i in d:
        city_list.append(i.get('name'))
    return city_list


def get_address(count=10):
    url = f'https://random-data-api.com/api/address/random_address?size={count}'
    response = requests.get(url, headers={'Accept': 'application/json'})
    data = response.json()
    address_list = []
    for address in data:
        address_list.append(f"{address['street_name']},{address['street_address']},{address['secondary_address']}")
    return address_list


def get_telephone():
    telephone_code = [29, 44, 33, 25]
    telephone = f"+375({rm.choice(telephone_code)}){rm.randint(1000000, 9999999)}"
    return telephone
