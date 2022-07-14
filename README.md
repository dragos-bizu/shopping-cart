# shopping-cart

## About The Project
This is an API for a shopping cart. The API is made in Django Rest Framework, the database that is using is an instance of PostgreSQL. It has endpoints for every CRUD operation on Products, add and remove from cart, create and return order, and endpoints for authentification. For security it uses django tokens for login into the app and for accesing private endpoints. The API is entirely dockerized.
The client application that makes calls to this API is made in python and it is a CLI application.

### Prerequisites
To use the API and Client Application you need to install [Docker](https://docs.docker.com/desktop/windows/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Gettin Started
* Before starting the server you have to create the docker image and run the tests to make sure everything is ok:
  ```sh
  docker-compose run app sh -c "python manage.py wait_for_db && python manage.py test"
  ```
* After you need the start the DRF server:
  ```sh
  docker-compose up app
  ```
* After the server is up and everything is generated you can start the Client Application:
  ```sh
  docker-compose run client sh -c "cd shopping-cart-client-app && python shopping-cart-app.py"
  ```
  
### Swagger
For swagger documention you have to access in your browser after the server is started [http://localhost:8000/swagger/](http://localhost:8000/swagger/).

### Client Application
Client Application is a CLI application made in python. With this application you can view active products, add to cart, search products and make an order.
The commands: (They are not case sensitive):
* Shows your money in the wallet.
  ```sh
  wallet
  ```
* Shows products list paginated, you can navigate through pages.
  ```sh
  products
  ```
* Search products by name.
  ```sh
  search products
  ```
* Shows your products saved in cart.
  ```sh
  cart
  ```
* Add product in cart.
  ```sh
  add to cart
  ```
* Remove product from your cart.
  ```sh
  remove from cart
  ```
* Place an order with all the items in cart.
  ```sh
  cart checkout
  ```
* Shows all your orders placed.
  ```sh
  orders
  ```
* Return product from your order.
  ```sh
  return product
  ```
* Close the application.
  ```sh
  exit
  ```
