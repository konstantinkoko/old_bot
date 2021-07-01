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
            message = 'this compay is already in the list'
        return message

    @check_password
    def show_company_list(self):
        return list(self.company_list)

user = User('konstantinko', '123')
print(user.show_company_list('konstantinko', '123'))
user.add_company('konstantinko', '123', 'GAZP')
print(user.show_company_list('konstantinko', '123'))
user.add_company('konstantinko', '123 ', 'MTS')
print(user.show_company_list('konstantinko', '123'))