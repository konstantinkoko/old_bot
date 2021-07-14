import requests
from bs4 import BeautifulSoup
import sqlite3 as sql

flag = True
id = 6686
#38312

with sql.connect('test_data_base.db') as connect:
    connect.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER NOT NULL PRIMARY KEY,
            company_name TEXT,
            ticker TEXT
        );
    """)

while id < 38312:
    r = requests.get('https://e-disclosure.ru/portal/company.aspx?id=' + str(id))

    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find("h2").text

    if 'Запрошенная страница не существует.' not in name:
        print(f'"{name}" : "{id}",')
        with sql.connect('test_data_base.db') as connect:
            connect.execute("""
                INSERT OR REPLACE INTO companies (company_id, company_name, ticker)
                VALUES(?,?,?);
            """, (id, name, None))
    id += 1
