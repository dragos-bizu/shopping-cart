# shopping-cart

## About The Project
This is an API for a shopping cart. The API is made in Django Rest Framework, the database that is using is an instance of PostgreSQL. It has endpoints for every CRUD operation on Products, add and remove from cart, create and return order, and endpoints for authentification. For security it uses django tokens for login into the app and for accesing private endpoints. The API is entirely dockerized.
The client application that makes calls to this API is made in python and it is a CLI application.

### Prerequisites
To use the API and Client Application you need to install [Docker](https://docs.docker.com/desktop/windows/install/) and [Docker Compose](https://docs.docker.com/compose/install/)

### Gettin Started
Before starting the server you have to create the docker image and run the tests to make sure everything is ok:
  ```sh
  docker-compose run app sh -c "python manage.py wait_for_db && python manage.py test"
  ```
After you need the start the DRF server:
  ```sh
  docker-compose up app
  ```
After the server is up and everything is generated you can start the Client Application:
  ```sh
  docker-compose run client sh -c "cd shopping-cart-client-app && python shopping-cart-app.py"
  ```
