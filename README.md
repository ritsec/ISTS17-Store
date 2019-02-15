# ISTS Store

This store is a combination of the following three previous application:

- [ISTS16-Ecommerce](https://github.com/RITSPARSA/ISTS16-ECommerce)
- [ISTS16-EcommerceBackend](https://github.com/RITSPARSA/ISTS16-ECommerceBackend)
- ISTS16-BankAPI - Which has magically disappeared


This is the WHITETEAM run store and should be secure. For ISTS17, we are
implementing a Whiteteam AD server which the blueteams will have an out-of-scope
account on. This store will interact with that.

## Running the application
To run the frontend and the backend for the store, simply call the following commands in the root
directory of the repository
```
docker-compose build
docker-compose up
```

## Adding items to the store
To add items to the store, update `items/items.yml` with a name, description, price, and image name.
Copy the image for the item to the `items` directory.

Rebuilt the docker-compose images and rerun the db script.