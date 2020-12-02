# Tumblr blog archiver

## Setup

Set up a virtual environment. This project uses python version 3.9.0. I like to use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/):

```
mkvirtualenv --python=python3.9 yourvirtualenvname
```

Then set up your environment variables:

```
cp .example.env archiver/.env
```

Replace dummy values with correct credentials for accessing the [Tumblr API](https://www.tumblr.com/docs/en/api/v2).

## Run

Apply migrations:

```
python ./manage.py migrate
```

Run the server:

```
python ./manage.py runserver
```

## More info

[Django docs](https://docs.djangoproject.com/en/3.1/)
