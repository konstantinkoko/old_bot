import requests
from bs4 import BeautifulSoup


flag = True
id = 14702
names = {}
#38312


while id < 38312:
    r = requests.get('https://e-disclosure.ru/portal/company.aspx?id=' + str(id))

    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find("h2").text

    if name != 'Запрошенная страница не существует.':
        names[str(id)] = name
        id_name = str(id) + ' = ' + name
        print(id_name)
        with open('id_names.txt', 'a', encoding='utf-8') as g:
            g.write(id_name + '\n')
    id += 1

'''

id = 999
r = requests.get('https://e-disclosure.ru/portal/company.aspx?id=' + str(id))

soup = BeautifulSoup(r.text, 'html.parser')
print(soup.find("h2").text)
'''