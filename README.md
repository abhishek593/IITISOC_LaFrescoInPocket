# LA FRESCO IN POCKET
### Project 
A website that has the following features:
1. Place an order
2. La Fresco staff will receive the order and generate a unique code.
3. A mail will be sent when order is ready to collect the package in a definite time slot.
In this way the number of contacts will be reduced and social distancing will be maintained.
---

### Technologies Used
Django  
Python 
### Install Requirements
First, create a python virtual environment. Then install requirements as-
```
pip install -r requirements.txt
```
### Setup
```
python manage.py makemigrations
python manage.py migrate
```
#### Creating superuser (for accessing Admin Website)
```
python manage.py createsuperuser
```
### Setup Sending Mail 
The settings file is currently set to send mails using **Gmail**.
> For **Gmail**  
> Set EMAIL_HOST_USER as your EMAIL Address and EMAIL_HOST_PASSWORD as your Email Address Password

### Serving static files
The project uses the library [**whitenoise**](http://whitenoise.evans.io/en/stable/django.html)
to serve the static files hassle free both in development and production.

### Usage
In development server  
Admin website -  'http://127.0.0.1:8000/admin'  
All the orders made lies under Orders section and can be filtered by their current status.  
User website - 'http://127.0.0.1:8000/'  
If used in production just change settings file
and use **PROTOCOL** as 'https' and **DOMAIN** as 'domain_name' 

## Optional
### Populating initial data-
A custom script which populates the database with **sections** and **items**
if you don't want them to add manually.
```
python manage.py add_product_data
``` 
The data used to populate database comes from 'product_dataset.json' file present in this
project's root directory.

