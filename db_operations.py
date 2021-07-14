import sqlite3 as sql
from aggregator import ticker_check

def add_user(id, name):
    with sql.connect('test_data_base.db') as connect:
        connect.execute("""
            INSERT OR IGNORE INTO user (user_id, name)
            VALUES(?,?);
        """, (id, name))

def add_company(id, ticker):
    ticker_info = ticker_check(ticker)  # [ticker_format, right_check, status]
    if ticker_info[1]:
        with sql.connect('test_data_base.db') as connect:
            connect.execute(f"""
                INSERT OR IGNORE INTO users_companies (user_id, ticker)
                VALUES(?,?);
                """, (id, ticker_info[0]))
    return ticker_info[2]

def remove_company(id, ticker):
    ticker_info = ticker_check(ticker)  # [ticker_format, right_check, status]
    with sql.connect('test_data_base.db') as connect:
        connect.execute(f"""
                DELETE FROM users_companies
                WHERE user_id = ? AND ticker = ?;
                """, (id, ticker_info[0]))
    return ticker_info[2]

def show_companies(id):
    with sql.connect('test_data_base.db') as connect:
        cursor = connect.execute(f"""
                SELECT * FROM users_companies
                WHERE user_id = ?;
                """, (id,))
        data = cursor.fetchall()
    return str(data)

def set_notification_time(id, time):
    status = 'ok'
    return status
