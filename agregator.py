import requests
from bs4 import BeautifulSoup

def event_list(id, year):
    r = requests.get('https://e-disclosure.ru/Event/Page?companyId=' + str(id) + '&year=' + str(year))

    soup = BeautifulSoup(r.text, 'html.parser')

    for i in soup.find_all("tr")[1:]:
        columns = i.find_all("td")
        if 'Изменение размера доли участия' in columns[2].text:
            date = columns[1].text.split()[0]
            time = columns[1].text.split()[1]
            event_info_url = columns[2].a['href']
            try:
                info = make_info(event_info_url, date, time)
            except:
                print('--------------------')
                print('нет данных')
            show_info(info)


def make_info(event_info_url, date, time):

    info_dict = {}
    info_dict['date'] = date
    info_dict['time'] = time
    info_dict['event_info_url'] = event_info_url
    r = requests.get(event_info_url)

    soup = BeautifulSoup(r.text, 'html.parser')
    info = soup.find("div", style="word-break: break-word; word-wrap: break-word;")
    for br in info.find_all('br'):
        text = br.next_sibling
        if str(text)[:4] =='2.1.':
            info_dict['name'] = ' '.join(text.strip('.').split()[-3:])
        if str(text)[:4] =='2.2.':
            info_dict['post'] = ' '.join(text.strip('.').split()[14:])
        if str(text)[:4] == '2.4.':
            info_dict['before'] = []
            for i in text.split():
                if '%' in i:
                    info_dict['before'].append(i.strip('–.'))
        if str(text)[:4] == '2.5.':
            info_dict['after'] = []
            for i in text.split():
                if '%' in i:
                    info_dict['after'].append(i.strip('–.'))
    return info_dict

def show_info(info):
    print('--------------------')
    print(info['date'])
    print(info['name'])
    print(info['post'])
    print('изменение доли акций:')
    print("{:f}".format(
        float(info['after'][1].strip('%').replace(',', '.')) - float(info['before'][1].strip('%').replace(',', '.'))),
          '%', sep='')
    print(info['event_info_url'])



id = 934
year = 2021
event_list(id, year)

