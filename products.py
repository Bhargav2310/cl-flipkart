"""Problem statement: Products
   Date: 24/09/20
   Author: Bhargav Andhe"""

from database import *
from main import clear


class Product:
    def __init__(self, id, name, price, category, stock=0, description=''):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock = stock

    def get_info(self):
        data = (self.id, self.name, self.price, self.stock, self.category, self.description)
        return data


def select(id):
    clear()
    print('=' * 25)
    print(f"You've selected {get_product_info('Name', id)}")
    print(f'Price: Rs. {get_product_info("Price", id)}/-')
    print(f'Description: {get_product_info("Description", id)}')
    quantity = int(get_product_info('Stock', id))
    if quantity == 0:
        print('Currently out of stock!')
    elif quantity <= 5:
        print(f'Only {quantity} units left in stock!')
    print('=' * 25)


def print_product(i, id, quantity=0):
    if i == 1:
        print('=' * 25)
    print(f'{i}) {get_product_info("Name", id)}')
    if quantity == 0:
        print(f'Price: Rs. {get_product_info("Price", id)}/-')
    else:
        print(f'In cart: {quantity} items.')
        print(f'Unit price: Rs.{get_product_info("Price", id)}')
        print(f'Total Price = Rs. {int(get_product_info("Price", id)) * quantity}')
    print(f'Description: {get_product_info("Description", id)}')
    print('=' * 25)


def show_products_by_category(category, current_user=None):
    ids = get_product_id(category)
    print(f'Showing available products in {category} category.')
    print('=' * 25)
    i = 1
    for id in ids:
        print(f'{i}) {get_product_info("Name", id)}')
        print(f'Price: Rs. {get_product_info("Price", id)}/-')
        print(f'Description: {get_product_info("Description", id)}')
        stock = int(get_product_info('Stock', id))
        if stock <= 0:
            print('Currently out of stock!')
        elif stock <= 5:
            print(f'Only {stock} units left in stock!')
        print('=' * 25)
        i += 1

    print('Hit ENTER for previous menu OR')
    choice = input('Enter serial no. of product to select: ')

    if choice == '':
        pass
    elif choice.isdecimal():
        choice = int(choice)
        if 0 < choice < i:
            selection = ids[choice - 1]
            select(selection)
            print('1. Add to cart\n2. Add to wishlist\n3. Previous menu')
            choice = input('Enter choice: ')

            if current_user is not None:
                if choice.isdecimal():
                    choice = int(choice)
                    if choice == 1:
                        quantity = input('Enter quantity: ')
                        if quantity.isdecimal():
                            quantity = int(quantity)
                            if quantity <= int(get_product_info('Stock', selection)):
                                add_to_cart(current_user, selection, quantity)
                            else:
                                print(f"Oops, We don't have {quantity} units!")
                                print(f'You can order a maximum of {get_product_info("Stock", selection)}')
                                print('Hit ENTER to continue')
                                input('>> ')
                                clear()
                                show_products_by_category(category, current_user)
                    elif choice == 2:
                        prev = get_wishlist(current_user)
                        if selection not in prev:
                            if prev == '':
                                final = selection
                            else:
                                final = prev + ',' + selection
                            add_to_wishlist(current_user, final)
                        else:
                            print('Item already exists in cart!')
                        print('Hit ENTER to for previous menu')
                        input('>> ')
                else:
                    print('Enter a valid choice!')
                    show_products_by_category(category)
            else:
                clear()
                print('You need to login/register first')
                return -1
        else:
            clear()
            print('Enter a valid serial number!')
            show_products_by_category(category)
    else:
        clear()
        print('Enter a valid serial number')
        show_products_by_category(category)
