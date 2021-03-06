import os
from getpass import getpass

from products import *
from user import User

current_user = None
user = None

fields = ['id', 'name', 'price', 'stock', 'category', 'description']


def clear():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')


def login_activity():
    id = input('Enter username/phone-number: ').lower()
    password = getpass('Enter password: ')
    if search_user_by('Username', id) or search_user_by('Phone', id):
        if password == get_user_data('Password', id):
            global current_user
            current_user = get_user_data('Username', id)
        else:
            print('Invalid Password!')
            if input('Would you like to try again(Y/N)? ')[0].lower() == 'y':
                login_activity()
            else:
                clear()
                show_menu()
    else:
        print('No such user found!')
        if input('Would you like to register(Y/N)? ')[0].lower() == 'y':
            register_activity()
        else:
            clear()
            show_menu()
    clear()
    show_menu()


def register_activity():
    global current_user
    username = input('Choose an username: ').lower()
    while search_user_by('Username', username):
        print('That username is already taken!')
        username = input('Choose another one: ')

    password = getpass('Choose a password: ')
    name = input('Enter your name: ')

    phone = input('Enter your phone-number: ')
    while search_user_by('Phone', phone):
        print('That phone-number already exists!')
        phone = input('Choose another one: ')

    age = int(input('Enter your age: '))
    gender = input('Enter your gender(M/F): ')[0].lower()

    email = input('Enter your email-address: ')
    while search_user_by('Email', email):
        print('That email address already exists!')
        email = input('Choose another one: ')

    print('Alright! Last step, set your address: ')
    address = input('>> ')

    # Creating a user object
    global user
    user = User(username, password, name, phone, age, gender, email, address)
    add_user(user)
    current_user = username


def admin():
    global current_user
    if current_user == 'admin':
        print(
            '1. Add new product\n2. Delete existing product\n3. Edit products\n4. Show all products\n5. Show all users\n6. Previous menu')
        choice = input('Enter choice: ')
        # Add new product
        if choice == '1':
            id = input('Enter an unique product ID: ')
            while product_exists(id):
                print('Product with same ID already exists!')
                id_ = input('Choose another ID or type "c" to cancel: ')
                if id_ == 'c':
                    clear()
                    admin()
                    pass
                else:
                    id = id_

            name = input('Enter product name: ')

            category = input('Enter the category: ')

            price = input('Enter price: ')
            if price.isdecimal():
                price = int(price)

            stock = input('Enter no. of items in stock: ')
            if stock.isdecimal():
                stock = int(stock)

            description = input('Enter product description(optional): ')
            product = Product(id, name, price, category, stock, description)

            add_product(product)
            print('Added successfully')
            print('Hit ENTER to continue')
            input('>> ')
        # Delete existing product
        elif choice == '2':
            id = input('Enter the product ID: ')
            name = get_product_info("Name", id)
            if input(f'Are you sure, you want to delete {name}(Y/N)? ')[0].lower() == 'y':
                remove_product(id)
            else:
                admin()
        # Edit existing product
        elif choice == '3':
            id = input('Enter the product ID: ')
            print(f"You've selected {get_product_info('Name', id)}")
            print('Available fields: ')
            print(fields)
            field = input('Enter the field to be edited: ').lower()
            if field in fields:
                if field == 'id':
                    init = get_product_info('ID', id)
                    print(f'Previous ID: {init}')
                    final = input('Enter new product ID: ')
                    update_product_data('ID', init, final)
                    print(f'Updated ID to {final}')
                elif field == 'name':
                    init = get_product_info('Name', id)
                    print(f'Previous name: {init}')
                    final = input('Enter new name: ')
                    update_product_data('Name', init, final)
                    print(f'Updated name to {final}')
                elif field == 'price':
                    init = get_product_info('Price', id)
                    print(f'Previous price: {init}')
                    final = float(input('Enter new price: '))
                    update_product_data('Price', init, final)
                    print(f'Updated price to Rs. {final}')
                elif field == 'stock':
                    init = get_product_info('Stock', id)
                    print(f'Previously in stock: {init}')
                    final = input('Enter no. of items to be added: ')
                    if final.isdecimal():
                        final = int(final)
                    final += init
                    update_product_data('Stock', init, final)
                    print(f'Updated stocks to {final}')
                elif field == 'description':
                    init = get_product_info('Description', id)
                    print(f'Previous description: {init}')
                    final = input('Enter a new description: ')
                    update_product_data('Description', init, final)
                    print('Successfully updated description!')
            else:
                print('No such field found!')
                admin()
        # Show all products
        elif choice == '4':
            print('Press ENTER to show all the products or type the category to filter products by category')
            fetch_all_products(input('>> '))
        # Show all users
        elif choice == '5':
            print('Press ENTER to show all the users or type the initial letters of the user to filter users')
            fetch_all_users(input('>> '))
        # Previous menu
        elif choice == '6':
            current_user = None
            clear()
            show_menu()
        else:
            print('Invalid choice, Try again!')
            print('Press ENTER to continue')
            input('>> ')
    else:
        print('You must be logged in as admin!')
        show_menu()


def show_categories():
    categories = get_existing_categories()
    for i in range(len(categories)):
        print(f'{i + 1}. {str(categories[i]).title()}')
    print('Hit ENTER for previous menu OR')
    choice = input('Enter choice: ')
    if choice == '':
        clear()
        show_menu()
    if choice.isdecimal():
        choice = int(choice)
        if 0 < choice <= len(categories):
            clear()
            flag = show_products_by_category(categories[choice - 1], current_user)
            if flag == -1:
                login_activity()

    else:
        print('Invalid choice, Try again!')
        print('Press ENTER to continue')
        input('>> ')
    clear()
    show_categories()


def wishlist(clr=False):
    if clr:
        clear()

    if current_user is not None:
        print(f'Showing wishlist of {current_user}')
        wishlist_string = get_wishlist(current_user)
        if wishlist_string == '':
            print('Your wishlist is currently empty!')
            print('Hit ENTER for main menu')
            input('>> ')
        else:
            wishlist_list = wishlist_string.split(',')
            i = 1
            for id in wishlist_list:
                print_product(i, id)
                i += 1
            print('1. Move items to cart\n2. Delete items from wishlist\n3. Previous menu')
            choice = input('Enter choice: ')

            if choice == '1':
                sr_no = input('Enter serial number of item: ')
                if sr_no.isdecimal():
                    sr_no = int(sr_no)
                    if 0 < sr_no <= len(wishlist_list):
                        quantity = input('Enter quantity: ')
                        in_stock = get_product_info('Stock', wishlist_list[sr_no - 1])
                        if in_stock >= int(quantity):
                            add_to_cart(current_user, wishlist_list[sr_no - 1], quantity)
                        else:
                            print(f"Oops, We don't have {quantity} units!")
                            print('You can add a maximum of ', in_stock, ' items!')
                            input('>> ')
                            wishlist(True)
                    else:
                        clear()
                        print('Invalid choice!')
                        wishlist()
                else:
                    clear()
                    print('Invalid choice!')
                    wishlist()
            elif choice == '2':
                sr_no = input('Enter Sr. no of item: ')
                if sr_no.isdecimal():
                    sr_no = int(sr_no)
                    if 0 < sr_no <= len(wishlist_list):
                        remove_from_wishlist(current_user, wishlist_list[sr_no - 1])
                        wishlist(True)
                    else:
                        clear()
                        print('Invalid choice!')
                        wishlist(True)
                else:
                    clear()
                    print('Invalid choice!')
                    wishlist()
            elif choice == '3':
                show_menu(True)
            else:
                clear()
                print('Invalid Choice!')
                wishlist()

    else:
        print('You are currently not logged in!')
        if input('Would you like to login(Y/N)? ')[0].lower() == 'y':
            login_activity()
        else:
            show_menu()
    show_menu(True)


def cart(clr=False):
    if clr:
        clear()

    if current_user is not None:
        print(f'Showing cart of {current_user}')
        cart_string = get_cart(current_user)
        if cart_string == '':
            print('Your cart is empty!')
            print('Hit ENTER for main menu')
            input('>> ')
        else:
            cart_total = 0
            cart_list = cart_string.split(',')
            i = 1
            for item in cart_list:
                id = item.split()[0]
                quantity = item.split()[1]
                if quantity.isdecimal():
                    quantity = int(quantity)
                    print_product(i, id, quantity)
                    price = int(get_product_info('Price', id)) * quantity
                    cart_total += price
                    i += 1
            print(f'\nTotal cart value: Rs. {cart_total}\n')
            print('1. To proceed for checkout\n2. To delete items from cart\n3. Previous menu')
            choice = input('Enter choice: ')
            if choice == '1':
                clear()
                confirmation = input(f'Proceed to pay Rs. {cart_total} (Y/N)? ')[0].lower()
                if confirmation == 'y':
                    remove_from_cart(current_user, 'all')
                    for item in cart_list:
                        reduce_stock(item.split()[0], int(item.split()[1]))
                    print(f'Order of Rs. {cart_total} successful!')
                    print('Keep shopping ....')
                    print('Hit ENTER to continue')
                    input('>> ')
                else:
                    cart(True)
            elif choice == '2':
                ids = [item.split()[0] for item in cart_list]
                sr_no = input('Enter the sr. no of product to be deleted: ')
                if sr_no.isdecimal():
                    sr_no = int(sr_no)
                    if 0 < sr_no <= len(ids):
                        remove_from_cart(current_user, ids[sr_no - 1])
                        cart(True)
                    else:
                        print('Enter a valid sr. no!')
                        cart(False)
                else:
                    print('Enter a valid sr. no!')
                    cart(False)
    else:
        print('You are currently not logged in!')
        if input('Would you like to login(Y/N)? ')[0].lower() == 'y':
            login_activity()
        else:
            clear()
            show_menu()
    clear()
    show_menu()


def profile():
    clear()
    global current_user, user
    if current_user is not None:
        user = User(get_user_data("Username", current_user),
                    get_user_data("Password", current_user),
                    get_user_data("Name", current_user),
                    get_user_data("Phone", current_user),
                    get_user_data("Age", current_user),
                    get_user_data("Gender", current_user),
                    get_user_data("Email", current_user),
                    get_user_data("Address", current_user))
        print('Your profile: ')
        print(f'Username: {user.username}')
        print(f'Name: {user.name}')
        print(f'Phone: {user.phone}')
        print(f'Age: {user.age}')
        print(f'Gender: {user.gender}')
        print(f'Email: {user.email}')
        print(f'Address: {user.address}')
        if input('Would you like to update your profile(Y/N)? ')[0].lower() == 'y':
            print('1. Change username\n2. Change password\n3. Change Name')
            print('4. Change Phone number\n5. Change email-address\n6. Change Address')
            choice = input('Enter your choice: ')
            if choice == '1':
                print(f'Previous username: {user.username}')
                username = input('Change to: ')
                while search_user_by('Username', username):
                    print('That username is already taken!')
                    username = input('Choose another one: ')
                update_user_data('Username', user.username, username)
                current_user = username
            elif choice == '2':
                password = input('Enter new password: ')
                update_user_data('Password', user.password, password)
            elif choice == '3':
                print(f'Previous name: {user.name}')
                name = input('Change to: ')
                update_user_data('Name', user.name, name)
            elif choice == '4':
                print(f'Previous phone-number: {user.phone}')
                phone = input('Change to: ')
                while search_user_by('Phone', phone):
                    print('That phone-number already exists!')
                    phone = input('Choose another one: ')
                update_user_data('Phone', user.phone, phone)
            elif choice == '5':
                print(f'Previous email: {user.email}')
                email = input('Change to: ')
                while search_user_by('Email', email):
                    print('That email address already exists!')
                    email = input('Choose another one: ')
                update_user_data('Email', user.email, email)
            elif choice == '6':
                print(f'Previous address: {user.address}')
                address = input('Change to: ')
                update_user_data('Address', user.address, address)
            else:
                print('Invalid choice!')
                profile()
        clear()
        show_menu()
    else:
        print('You are currently not logged in!')
        if input('Would you like to login(Y/N)? ')[0].lower() == 'y':
            login_activity()
        else:
            show_menu()


def log_out():
    global current_user
    current_user = None


def show_menu(clr=False):
    if clr:  # If clr == True, clear the screen
        clear()

    if current_user is not None:
        print(f'Logged in as {get_user_data("Name", current_user)}!')
    else:
        print(f'Please login or register to continue')
    print('1. Existing user? Login')
    print('2. New user? Register')
    print('3. Admin Login')
    print('4. Shop by Category')
    print('5. Wishlist')
    print('6. Cart')
    print('7. Profile')
    print('8. Log out')
    print('9. Exit')
    choice = input('Enter choice: ')
    clear()
    if choice == '1':
        login_activity()
    elif choice == '2':
        register_activity()
    elif choice == '3':
        admin()
    elif choice == '4':
        show_categories()
    elif choice == '5':
        wishlist(True)
    elif choice == '6':
        cart(True)
    elif choice == '7':
        profile()
    elif choice == '8':
        log_out()
        print('Logout successful....')
    elif choice == '9':
        print('Nice to see you stopping by!\nExiting....')
        exit(0)
    else:
        print('Invalid choice, try again!')
        show_menu()
    clear()
    show_menu()


if __name__ == '__main__':
    show_menu()
