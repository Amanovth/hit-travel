import requests


def country_list():
    countries = requests.get(
        'http://tourvisor.ru/xml/list.php?type=country&authlogin=info@hit-travel.kg&authpass=qbJbXlT1pBrL&format=json'
    ).json()['lists']['countries']['country']

    url = 'http://localhost:8000/country/create'

    for country in countries:
        r = requests.post(url, data={
            'sub_id': country['id'],
            'name': country['name']
        })
        print(r.text)


def departure_list():
    data = requests.get(
        'http://tourvisor.ru/xml/list.php?type=departure&authlogin=info@hit-travel.kg&authpass=qbJbXlT1pBrL&format=json'
    ).json()


country_list()
