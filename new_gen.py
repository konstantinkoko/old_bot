class User:
    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.__password = user_password
        self.company_list = {}

    def check_password(method_to_decorate):
        def wrapper(self, name, password, *args, **kwargs):
            if (name == self.user_name) and (password == self.__password):
                return method_to_decorate(self, *args, **kwargs)
            else:
                return print('wrong login or password')
        return wrapper

    @check_password
    def add_company(self, ticket):
        if ticket not in self.company_list:
            self.company_list[ticket] = {}
            message = 'sucsess'
        else:
            message = 'this company is already in the list'
        return message

    @check_password
    def del_company(self, ticket):
        if ticket in self.company_list:
            del self.company_list[ticket]
            message = 'sucsess'
        else:
            message = 'this company is not in the list'
        return message

    @check_password
    def show_company_list(self):
        return list(self.company_list)

import sqlite3 as sql

with sql.connect('test_data_base.db') as connect:
    connect.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            company_list TEXT
        );
    """)
    connect.execute("""
        CREATE TABLE IF NOT EXISTS users_companies (
            id INTEGER NOT NULL,
            ticket TEXT,
            CONSTRAINT p_key PRIMARY KEY (id, ticket)
        );
    """)

user = User('konstantinko', '123')
print(user.show_company_list('konstantinko', '123'))
user.add_company('konstantinko', '123', 'GAZP')
print(user.show_company_list('konstantinko', '123'))
user.add_company('konstantinko', '123', 'MTS')
print(user.show_company_list('konstantinko', '123'))