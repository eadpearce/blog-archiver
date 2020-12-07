# Tumblr blog archiver

Do you have a tumblog you've spent years curating that you'd like to archive so you can look through it offline? This may be the handy tool for you.

## Requirements

* Python 3.9

## Setup

Set up a virtual environment. I like to use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/):

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
