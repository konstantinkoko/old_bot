import requests
from bs4 import BeautifulSoup

def ticker_check(ticker):
    response = requests.get(f"https://iss.moex.com/iss/securities/{ticker}.json")  # https://iss.moex.com/iss/reference/
    company_info = response.json()
    right_check = False
    if len(company_info["description"]["data"]) > 0:
        currency = company_info["description"]["data"][7][2]
        ticker = company_info["description"]["data"][0][2]
        #type = company_info["description"]["data"][19][2]
        if currency != "SUR":
            status = "не в рублях"
        #elif "Акции" not in type:
        #    status = "не акции"
        else:
            status = "ok"
            right_check = True
    else:
        status = "тикер не найден"
    return [ticker, right_check, status]

def get_company_id(ticker):
    pass
    #return company_id

def show_company_trading_info(ticker, period='year'):
    ticker_info = ticker_check(ticker)  # [ticker_format, right_check, status]
    info = event_list(ticker_info[1], year=2021)
    return str(info)

def event_list(company_id, year):
    r = requests.get('https://e-disclosure.ru/Event/Page?companyId=' + str(company_id) + '&year=' + str(year))

    soup = BeautifulSoup(r.text, 'html.parser')

    info = []
    for i in soup.find_all("tr")[1:]:
        columns = i.find_all("td")
        if 'Изменение размера доли участия' in columns[2].text:
            date = columns[1].text.split()[0]
            time = columns[1].text.split()[1]
            event_info_url = columns[2].a['href']
            try:
                info += make_event_info(event_info_url, date, time)
            except:
                info += 'no data'
    return info

def make_event_info(event_info_url, date, time):

    info_dict = {'date': date, 'time': time, 'event_info_url': event_info_url}
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
