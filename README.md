# shopping-cart

##About The Project
This is an API for a shopping cart. The API is made in Django Rest Framework, the database that is using is an instance of PostgreSQL. It has endpoints for every CRUD operation on Products, add and remove from cart, create and return order, and endpoints for authentification. For security it uses django tokens for login into the app and for accesing private endpoints. The API is entirely dockerized.
The client application that makes calls to this API is made in python and it is a CLI application.

### Prerequisites
To use the API and Client Application you need to install [Docker](https://docs.docker.com/desktop/windows/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
