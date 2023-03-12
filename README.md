# Lending platform IMS

### Technologies used

Python 3.9.13

djangorestframework 3.14.0

### Setup and installtion

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