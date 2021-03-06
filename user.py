"""Problem statement: User
   Date: 25/09/20
   Author: Bhargav Andhe"""


class User:
    def __init__(self, username, password, name, phone, age, gender, email, address, wishlist='', cart=''):
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
        self.age = age
        self.gender = gender
        self.email = email
        self.address = address
        self.wishlist = wishlist
        self.cart = cart

    def get_all_data(self):
        return self.username, self.password, self.name, self.phone, self.age, self.gender, self.email, self.address, self.wishlist, self.cart
