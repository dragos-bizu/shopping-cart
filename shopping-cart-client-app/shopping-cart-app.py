import requests
import math
import datetime
from constants import APIPath


class ShoppingCartApplication:
    def __init__(self):
        self.headers = {}

    def start(self):
        print('Welcome to Shopping Cart Application')
        while not self.headers:
            self.sign_in()
        while True:
            command = input('')
            if command == 'exit':
                return
            self.command_manager(command)

    def sign_in(self):
        username = 'tim'
        password = 'tim12345'
        data = {'username': username, 'password': password}
        response = requests.post(f'{APIPath}/api/auth/token/', json=data)
        if response.status_code != 200:
            return print(f'Authentication failed! \n {response.json()}')
        print('Login successfully!')
        response = response.json()
        self.headers['Authorization'] = f'Token {response["token"]}'
        print('Use \'help\' for commands')

    def command_manager(self, command):
        if command.lower() == 'wallet':
            return self.wallet()
        if command.lower() == 'products':
            return self.products()
        if command.lower() == 'search products':
            return self.search_products()
        if command.lower() == 'cart':
            return self.cart()
        if command.lower() == 'add to cart':
            return self.add_to_cart()
        if command.lower() == 'remove from cart':
            return self.remove_from_cart()
        if command.lower() == 'cart checkout':
            return self.cart_checkout()
        if command.lower() == 'orders':
            return self.orders()
        if command.lower() == 'return product':
            return self.orders_return()
        if command.lower() == 'help':
            return self.help()
        else:
            print('Unknown command, use \'help\' to view all commands')

    def wallet(self):
        response = requests.get(f'{APIPath}/api/auth/me', headers=self.headers)
        if response.status_code != 200:
            return print(f'An error occurred! code: {response.status_code}')
        response = response.json()
        print(f'Your wallet: {response["wallet"]}$')

    def print_product(self, product):
        print(f'{product["sku"]}')
        print(f'Product ID: {product["id"]}')
        print(f'Name: {product["name"]}')
        print(f'Price: {product["price"]}$')
        print(f'Description: {product["description"]}')
        print(f'Delivery time: {product["delivery_time_days"]} days')
        print(f'Sizes: \n'
              f'    XS: {product["get_sizes"]["XS"]}  '
              f'ID: {product["get_sizes"]["XS_id"]}\n'
              f'    S: {product["get_sizes"]["S"]}  '
              f'ID: {product["get_sizes"]["S_id"]}\n'
              f'    M: {product["get_sizes"]["M"]}  '
              f'ID: {product["get_sizes"]["M_id"]}\n'
              f'    L: {product["get_sizes"]["L"]}  '
              f'ID: {product["get_sizes"]["L_id"]}\n'
              f'    XL: {product["get_sizes"]["XL"]}  '
              f'ID: {product["get_sizes"]["XL_id"]}\n')
        print('-----------------------------')

    def print_cart_product(self, product):
        print(f'{product["product"]["sku"]}')
        print(f'Product ID: {product["product"]["id"]}')
        print(f'Name: {product["product"]["name"]}')
        print(f'Price: {product["product"]["price"]}$')
        print(f'Description: {product["product"]["description"]}')
        print(
            f'Delivery time: {product["product"]["delivery_time_days"]} days')
        print(f'Size: {product["product_size"]["size"]}')
        print(f'Quantity: {product["quantity"]}\n')

    def products(self):
        print('---------PRODUCTS---------')
        page = 1
        while True:
            response = requests.get(f'{APIPath}/api/products/all/?page={page}')
            if response.status_code != 200:
                return print(
                    f'An error occurred! code: {response.status_code}')
            response = response.json()
            last_page = math.ceil(response['count'] / 10)
            for product in response['results']:
                self.print_product(product)

            print(f'Page: {page} / {last_page}')
            print('Enter next page number or exit:')
            page = input('Page: ')
            if page == 'exit':
                return
            while int(page) > last_page or int(page) < 1:
                print('Page number out of range!')
                page = input('Page: ')
                if page == 'exit':
                    return

    def cart(self):
        print('---------YOUR CART---------')
        page = 1
        while True:
            response = requests.get(f'{APIPath}/api/cart/details/?page={page}',
                                    headers=self.headers)
            if response.status_code != 200:
                return print(
                    f'An error occurred! code: {response.status_code}')
            response = response.json()
            last_page = math.ceil(response['count'] / 10)
            if response['count'] == 0:
                print('Your cart is empty!')
                return
            for product in response['results']['products']:
                print(f'Cart Item ID: {product["id"]}')
                self.print_cart_product(product)
                print('-----------------------------')
            print(f'Total Price: {response["results"]["total_price"]}$')
            print(f'Page: {page}/{last_page}')
            if last_page == page:
                return
            print('Enter next page number or exit:')
            page = input('Page: ')
            if page == 'exit':
                return
            while int(page) > last_page or int(page) < 1:
                print('Page number out of range!')
                page = input('Page: ')

    def add_to_cart(self):
        product_id = input('Enter Product ID: ')
        product_size_id = input('Enter Size ID: ')
        quantity = input('Enter quantity: ')
        data = {'product': product_id,
                'product_size': product_size_id,
                'quantity': quantity}
        response = requests.post(f'{APIPath}/api/cart/add/',
                                 headers=self.headers, data=data)
        if response.status_code != 201:
            if response:
                return print(f'{response.json()["Response"]}! '
                             f'code: {response.status_code}')
            return print(f'An error occurred! code: {response.status_code}')
        print('Item successfully added to cart!')

    def remove_from_cart(self):
        self.cart()
        cart_item_id = input('Enter the cart item ID you want to remove: ')
        data = {'cart_item_id': cart_item_id}
        response = requests.delete(f'{APIPath}/api/cart/add/',
                                   headers=self.headers, data=data)
        if response.status_code != 200:
            if response:
                return print(f'{response.json()["Response"]}! '
                             f'code: {response.status_code}')
            return print(f'An error occurred! code: {response.status_code}')
        print('Item successfully removed from cart!')

    def cart_checkout(self):
        self.cart()
        self.wallet()
        ans = input('Are you sure you want to checkout? [y/n]: ')
        while ans != 'y' and ans != 'n':
            ans = input('Are you sure you want to checkout? [y/n]: ')
        if ans == 'n':
            return
        response = requests.get(f'{APIPath}/api/cart/checkout/',
                                headers=self.headers)
        if response.status_code != 200:
            if response:
                return print(f'{response.json()["Response"]}! '
                             f'code: {response.status_code}')
            return print(f'An error occurred! code: {response.status_code}')

        print('Order placed successfully!')

    def orders(self):
        print('---------YOUR ORDERS---------')
        response = requests.get(f'{APIPath}/api/order/', headers=self.headers)
        if response.status_code != 200:
            return print(
                f'An error occurred! code: {response.status_code}')
        response = response.json()
        if not response:
            return print('You have no orders placed!')

        for order in response:
            placed_at = datetime.datetime.strptime(order['created_at'],
                                                   '%Y-%m-%dT%H:%M:%S.%f')
            print(f'Order placed at: '
                  f'{placed_at.utcnow().strftime("%d/%m/%Y %H:%M")}')
            for order_item in order['get_items']:
                print(f'    Order Item ID: {order_item["id"]}')
                self.print_cart_product(order_item)
                print(f'    Status: {order_item["status"]}\n')
                print('-----------------------------')
            print(f'Total price: {order["total_price"]}')
            print('-----------------------------')

    def orders_return(self):
        order_item_id = input('Enter Order Item ID:')
        data = {'order_item_id': order_item_id}

        ans = input('Are you sure you want to return this item? [y/n]: ')
        while ans != 'y' and ans != 'n':
            ans = input('Are you sure you want to return this item? [y/n]: ')
        if ans == 'n':
            return
        response = requests.put(f'{APIPath}/api/order/return/',
                                headers=self.headers, data=data)
        if response.status_code != 200:
            if response:
                return print(f'{response.json()["Response"]}! '
                             f'code: {response.status_code}')
            return print(f'An error occurred! code: {response.status_code}')
        print('Item successfully returned, and your money returned!')

    def search_products(self):
        search = input('Enter product name you want to search: ')
        print(f'---------PRODUCTS {search}---------')
        page = 1
        while True:
            response = requests.get(f'{APIPath}/api/products/all/?page={page}'
                                    f'&search={search}')
            if response.status_code != 200:
                return print(
                    f'An error occurred! code: {response.status_code}')
            response = response.json()
            last_page = math.ceil(response['count'] / 10)
            for product in response['results']:
                self.print_product(product)

            print(f'Page: {page} / {last_page}')
            print('Enter next page number or exit:')
            page = input('Page: ')
            if page == 'exit':
                return
            while int(page) > last_page or int(page) < 1:
                print('Page number out of range!')
                page = input('Page: ')
                if page == 'exit':
                    return

    def help(self):
        print('     Commands (are not case sensitive):')
        print('wallet    Shows your money in the wallet.')
        print('products    Shows products list paginated, '
              'you can navigate through pages.')
        print('search products    Search products by name.')
        print('cart    Shows your products saved in cart.')
        print('add to cart    Add product in cart.')
        print('remove from cart    Remove product from your cart.')
        print('cart checkout   Place an order with all the items in cart')
        print('orders    Shows all your orders placed')
        print('return product    Return product from your order')
        print('exit    Close the application')


app = ShoppingCartApplication()
app.start()
