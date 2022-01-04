# POS
APIs designed for a point of sale (POS) system. The POS system has the capability to control the menu and perform CRUD operations also which can place an order successfully by validating the payment correctness and item availability
* Dev environment uses Docker and Docker compose.
# Development environment setup
| tool  | version |
| ----- | ------- |
 | docker-compose | 1.29.x |
 | docker | 20.10.x |
* ```git clone https://github.com/HimavarshaVS/POS.git```
* Switch to project directory ```cd POS```
* Once you are in the root directory of the project run```docker-compose up --build -d``` to build the image and start the app. 
* This will download and provision two containers: one running PostgreSQL and other running the Flask app. Initial run will take a while but the subsequent runs will be faster
* When docker-compose up completes, the app should be accessible at http://127.0.0.1:8085

# Project organization
* Application-wide settings are stored in config.py at the root of the repository. These items are accessible on the config dictionary property of the app object.
* The directory /app contains the API application
* URL mapping is managed in /app/routers/__init__.py
* Functionality is organized in packages. Example: /app/routers/menu
* Tests are contained in each package. Example: app/test_items.py

# API Documentation
API Documentation can be accessible at http://127.0.0.1:8085/v1/api-doc
![swagger_pos](https://user-images.githubusercontent.com/40851462/148033881-253b0411-5fd9-488a-a5e7-f719ce39f816.png)
