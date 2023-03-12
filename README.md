# Lending platform IMS

## Technologies used

Python 3.9.13

djangorestframework 3.14.0

## Setup and installtion

- Install Python 3

  [Python installation guide](https://www.python.org/downloads/)


- Install virtualenv

```bash
python -m pip install --user virtualenv
```

- Create and activate virtual environment

```shell
virtualenv -p python3 env
source env/bin/activate
```

- Install requirements

```bash
pip install -r requirements.txt
```

- Make migrations and migrate

```shell
python manage.py makemigrations
python manage.py migrate
```

- Create admin

```shell
python manage.py createsuperuser
```

- Start development server

```shell
python manage.py runserver
```

- Testing

```shell
python manage.py test
```

- Coverage
```shell
python manage.py test --with-coverage
```

##Working with Api example
Register Customer
```shell
curl --location --request POST 'http://127.0.0.1:8000/user/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"customer55@gmail.com",
    "password":"Mypassrd91"
}'
```

Customer Login
```shell
curl --location --request POST 'http://127.0.0.1:8000/user/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"customer55@gmail.com",
    "password":"Mypassrd91"
}'
```
Create customer profile
```shell
curl --location --request POST 'http://127.0.0.1:8000/customer/' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "full_name":"customer name"
}'
```

Update customer profile
```shell
curl --location --request PUT 'http://127.0.0.1:8000/customer/88e53381-4185-4492-93f0-358878508063' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "full_name":"customer name 2"
}'
```
Create Loan products (admin only)

How to create admin
```shell
python manage.py createsuperuser
```
```shell
curl --location --request POST 'http://127.0.0.1:8000/lending/product' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4NjU5NzA5LCJpYXQiOjE2Nzg2NTYxMDksImp0aSI6ImVhZDc0MDljNzc2ODQ2OTI4ODFlMDQyMDdkZDYxMDI3IiwidXNlcl9pZCI6IjZkMGZmOGFmLWRhNzItNDMxYS1hYjE5LTBlMzk4M2QzZmQ2NCJ9.BMWMoQd1fTSKu1vmqF_mlt-IeZOxtxu3KyRcR3Ec1nA' \
--header 'Content-Type: application/json' \
--data-raw '{
        "product_name": "Product A",
        "loan_limit": "1000.00",
        "interest_rate": "10.00",
        "duration": 15,
        "notification_channel": "ALL"
    }'
```
Create mobile wallet
```shell
curl --location --request POST 'http://127.0.0.1:8000/customer/mobile-wallet' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"254789665345"
}'
```

Update mobile wallet
```shell
curl --location --request PUT 'http://127.0.0.1:8000/customer/mobile-wallet/5cb5fe6d-45b7-44e3-9bc1-732071a6fe83' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone_number":"254789665349"
}'
```
Get mobile wallet
```shell
curl --location --request GET 'http://127.0.0.1:8000/customer/mobile-wallet/5cb5fe6d-45b7-44e3-9bc1-732071a6fe83' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--data-raw ''
```
View loan products
```shell
curl --location --request GET 'http://127.0.0.1:8000/lending/product' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--data-raw ''
```

Create loan offer
```shell
curl --location --request POST 'http://127.0.0.1:8000/customer/loan-offer' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "loan_product_id": "adace270-cc75-48f3-a79f-e81be86d6ed6",
    "amount": 500
}'
```

Get loan offers
```shell
curl --location --request GET 'http://127.0.0.1:8000/customer/loan-offer' \
--header 'Authorization: Bearer {ACCESS_TOKEN}'
```

Pay loan manually
```shell
curl --location --request POST 'http://127.0.0.1:8000/customer/pay-loan' \
--header 'Authorization: Bearer {ACCESS_TOKEN}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "loan_offer_id": "0b8d3505-eb39-4a38-b4c6-63d99a489a4a",
    "amount": 500
}'
```

