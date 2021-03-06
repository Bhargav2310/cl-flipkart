"""Problem statement: Database
   Date: 24/09/20
   Author: Bhargav Andhe"""
import sqlite3


def create_user_table_if_not_exists(conn):
    """creates a USERS table if not exists"""

    cursor = conn.cursor()
    cmd = '''CREATE TABLE IF NOT EXISTS USERS (
                        Username TEXT,
                        Password TEXT,
                        Name TEXT,
                        Phone TEXT,
                        Age INTEGER,
                        GENDER CHAR,
                        Email TEXT,
                        Address TEXT,
                        Wishlist TEXT,
                        Cart TEXT
                        )'''
    cursor.execute(cmd)
    conn.commit()


def search_user_by(column, credentials):
    """If credentials found in selected column, returns True
        Else, returns False"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_user_table_if_not_exists(conn)

    cmd = f'''SELECT {column} from USERS'''
    cursor.execute(cmd)

    fetched_data = cursor.fetchall()
    for data in fetched_data:
        for x in data:
            if x == credentials:
                return True
    return False


def add_user(user):
    """takes User class object as parameter and add it to database"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_user_table_if_not_exists(conn)

    cmd = '''INSERT INTO USERS (Username, Password, Name, Phone, Age, Gender, Email, Address, Wishlist, Cart) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    cursor.execute(cmd, user.get_all_data())
    conn.commit()


def get_user_data(field, id):
    """:returns string of user data if user found in database"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_user_table_if_not_exists(conn)

    cmd = f'''SELECT {field} FROM USERS WHERE Username="{id}" OR Phone="{id}"'''
    cursor.execute(cmd)
    data = cursor.fetchone()
    if data is not None:
        return data[0]


def update_user_data(field, init, final):
    """updates certain properties of user from init value to final value"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_user_table_if_not_exists(conn)

    cmd = f'''UPDATE USERS SET {field}="{final}" WHERE {field}="{init}"'''
    cursor.execute(cmd)
    conn.commit()


def create_product_table_if_not_exists(conn):
    """creates a PRODUCTS table if not exists"""

    cursor = conn.cursor()
    cmd = '''CREATE TABLE IF NOT EXISTS PRODUCTS (
                    ID TEXT,
                    Name TEXT,
                    Price REAL,
                    Stock INTEGER,
                    Category TEXT,
                    Description TEXT
                  )'''
    cursor.execute(cmd)
    conn.commit()


def add_product(product):
    """takes product class object as parameter and adds that product to database"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    cmd = '''INSERT INTO PRODUCTS (ID, Name, Price, Stock, Category, Description) VALUES (?, ?, ?, ?, ?, ?)'''
    cursor.execute(cmd, product.get_info())
    conn.commit()


def product_exists(id):
    """If product is found in selected column, returns True
        Else, returns False"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    cmd = '''SELECT ID from PRODUCTS'''
    cursor.execute(cmd)

    fetched_data = cursor.fetchall()
    for data in fetched_data:
        for x in data:
            if x == id:
                return True
    return False


def get_product_info(field, id):
    """takes field and product id as parameters and returns info about product"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    cmd = f'''SELECT {field} FROM PRODUCTS WHERE ID="{id}"'''
    cursor.execute(cmd)
    return cursor.fetchone()[0]


def update_product_data(field, init, final):
    """updates certain properties of product from init value to final value"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    cmd = f'''UPDATE PRODUCTS SET {field}="{final}" WHERE {field}="{init}"'''
    cursor.execute(cmd)
    conn.commit()


def remove_product(id):
    """takes the product id and removes it from database"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    cmd = f'DELETE FROM PRODUCTS WHERE ID="{id}"'
    cursor.execute(cmd)
    conn.commit()


def fetch_all_products(category=''):
    """prints all the products if category=''  or prints products of specific category if category!=''"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    if str(category.strip()) == '':
        cmd = '''SELECT ID, Name FROM PRODUCTS'''
    else:
        cmd = f'''SELECT ID, Name FROM PRODUCTS WHERE Category="{category}"'''
    cursor.execute(cmd)

    fetched_data = cursor.fetchall()
    print('(ID, Name)')
    for data in fetched_data:
        print(data)

    input('\nPress ENTER to continue ....')


def fetch_all_users(init=''):
    """prints all the users in database"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_user_table_if_not_exists(conn)

    cmd = '''SELECT Username FROM USERS'''

    cursor.execute(cmd)
    fetched_data = cursor.fetchall()
    users = []
    for data in fetched_data:
        for x in data:
            if init != '':
                if str(x).lower().startswith(init.lower()):
                    users.append(x)
            else:
                users.append(x)
    print(users)

    input('\nPress ENTER to continue ....')


def get_product_id(category=''):
    """takes category name of products and returns list of ids of product(s) having same category"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    create_product_table_if_not_exists(conn)

    if str(category.strip()) == '':
        cmd = '''SELECT ID FROM PRODUCTS'''
    else:
        cmd = f'''SELECT ID FROM PRODUCTS WHERE Category="{category}"'''
    cursor.execute(cmd)

    fetched_data = cursor.fetchall()
    ids = []
    for data in fetched_data:
        ids.append(data[0])

    return ids


def get_existing_categories() -> list:
    """:returns list of categories that are in the database"""

    conn = sqlite3.connect('database.db')
    cmd = '''SELECT Category FROM PRODUCTS'''
    cursor = conn.cursor()
    cursor.execute(cmd)

    data = cursor.fetchall()
    categories = []
    for category in data:
        if category[0] not in categories:
            categories.append(category[0])
    return categories


def get_wishlist(user) -> str:
    """:returns the wishlist string of current user"""

    conn = sqlite3.connect('database.db')
    cmd = f'''SELECT Wishlist FROM USERS WHERE Username="{user}"'''

    cursor = conn.cursor()
    cursor.execute(cmd)

    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]
    else:
        return ''


def get_cart(user) -> str:
    """:returns the cart string of current user"""

    conn = sqlite3.connect('database.db')
    cmd = f'SELECT Cart FROM USERS WHERE Username="{user}"'
    cursor = conn.cursor()
    cursor.execute(cmd)

    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]
    else:
        return ''


def add_to_wishlist(user, string):
    """takes the current username and product id to be added to wishlist"""

    conn = sqlite3.connect('database.db')
    cmd = f'''UPDATE USERS SET Wishlist="{string}" WHERE Username="{user}"'''

    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    print('Added to Wishlist')


def add_to_cart(user, string, quantity='1'):
    """takes the current username, product id and quantity to be added to cart"""

    conn = sqlite3.connect('database.db')
    init_cart = get_cart(user)
    if init_cart == '':
        final = string + ' ' + str(quantity)
        cmd = f'''UPDATE USERS SET Cart="{final}" WHERE Username="{user}"'''
        cursor = conn.cursor()
        cursor.execute(cmd)
    else:
        if init_cart.__contains__(','):
            init_cart = init_cart.split(',')
            ids = [item.split()[0] for item in init_cart]
            units = [int(item.split()[1]) for item in init_cart]

            if string in ids:
                units[ids.index(string)] += int(quantity)
            else:
                ids.append(string)
                units.append(int(quantity))

            final = ''
            for i in range(len(ids) - 1):
                final += ids[i] + ' ' + str(units[i]) + ','
            final += ids[-1] + ' ' + str(units[-1])
            cmd = f'''UPDATE USERS SET Cart="{final}" WHERE Username="{user}"'''
            cursor = conn.cursor()
            cursor.execute(cmd)
        else:
            ids, units = [], []
            ids.append(init_cart.split()[0])
            units.append(int(init_cart.split()[1]))

            if string in ids:
                units[ids.index(string)] += int(quantity)
                final = string + ' ' + str(units[0])
            else:
                ids.append(string)
                units.append(int(quantity))
                final = ids[0] + ' ' + str(units[0]) + ',' + ids[1] + ' ' + str(units[1])

            cmd = f'''UPDATE USERS SET Cart="{final}" WHERE Username="{user}"'''
            cursor = conn.cursor()
            cursor.execute(cmd)

    conn.commit()

    print(f'Added {get_product_info("Name", string)} to Cart of {user}')
    print('Hit ENTER to continue')
    input('>> ')


def remove_from_wishlist(user, string):
    """takes the current username and product id that is to be removed from wishlist"""

    prev = get_wishlist(user)
    if prev.__contains__(','):
        prev = prev.split(',')

        final = ''
        if string in prev:
            prev.remove(string)

            for id in prev[:-1]:
                final += id + ','
            final += prev[-1]
    else:
        final = ''

    add_to_wishlist(user, final)
    print(f'Removed {string} from wishlist of {user}')
    print('Hit ENTER to continue')
    input('>> ')


def remove_from_cart(user, string):
    """takes the current username and product id that is to be removed from cart"""

    if string == 'all':
        final = ''
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cmd = f'''UPDATE USERS SET Cart="{final}" WHERE Username="{user}"'''
        cursor.execute(cmd)
        conn.commit()
    else:
        prev = get_cart(user)
        final = ''
        if prev.__contains__(','):
            prev = prev.split(',')

            for item in prev:
                if item.__contains__(string):
                    prev.remove(item)

            if len(prev) == 1:
                final = prev[0]
            else:
                for item in prev[:-1]:
                    final += item + ','
                final += prev[-1]
        else:
            if prev.__contains__(string):
                final = ''

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cmd = f'''UPDATE USERS SET Cart="{final}" WHERE Username="{user}"'''
        cursor.execute(cmd)
        conn.commit()

        print(f'Removed {get_product_info("Name", string)} from Cart of {user}')
        print('Hit ENTER to continue')
        input('>> ')


def reduce_stock(id, units):
    """takes the id and no. of units to be removed from stock"""

    init_stock = get_product_info('Stock', id)
    final_stock = init_stock - units

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cmd = f'''UPDATE PRODUCTS SET Stock="{final_stock}" WHERE ID="{id}"'''

    cursor.execute(cmd)
    conn.commit()
