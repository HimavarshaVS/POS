![swagger_pos](https://user-images.githubusercontent.com/40851462/147994520-9f1d9330-8c65-4fdd-998c-a5db4c3424ff.png)
# POS
APIs designed for a point of sale (POS) system. The POS system has the capability to control the menu and perform CRUD operations also which can place an order successfully by validating the payment correctness and item availability


# Development environment
* Dev environment uses Docker and Docker compose.
* Project comes along with sample data which is loaded to db during app initialization

* ```docker-compose up -d``` to start the app. This will download and provision two containers: one running PostgreSQL and one running the Flask app. This will take a while, but once it completes subsequent launches will be much faster

* When docker-compose up completes, the app should be accessible at http://127.0.0.1:8085
# Run locally with docker
Use docker-compose

```commandline
docker-compose up -d
```

# Project organization
* Application-wide settings are stored in config.py at the root of the repository. These items are accessible on the config dictionary property of the app object. Example: debug = app.config['DEBUG']
* The directory /app contains the API application
* URL mapping is managed in /app/routers/__init__.py
* Functionality is organized in packages. Example: /app/routers/menu
* Tests are contained in each package. Example: app/test_items.py

# API Documentation
API Documentation can be accessible at http://127.0.0.1:8085
