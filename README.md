# Swapp

[![Build Status](https://travis-ci.com/Flagoul/swapp.svg?token=EpMgztqGsgqLdu8HDosP&branch=master)](https://travis-ci.com/Flagoul/swapp)

## Description

A project developped at HEIG-VD in the PDG course in a team of 5 people:
[Sébastien Boson](https://github.com/sebastie-boson), [Antoine Drabble](https://github.com/servietsky777), [Sébastien Richoz](https://github.com/sebastienrichoz), [Mathieu Urstein](https://github.com/MathieuUrstein) and [Basile Vu](https://github.com/Flagoul).

It consists in a web platform on which users can trade objects. Various filters are provided to find objects, such as object proximity, price range, categories and so on.

## Installation

### Prerequisites
- Python 3.6
- npm 3.10.10
- Sass 3.5.1

### Installation steps
Begin by cloning the repo and go into it:
```
$ git clone git@github.com:Flagoul/swapp.git
$ cd swapp
```
#### Install backend dependencies
Before running the command below, you may want to setup a [virtualenv](https://virtualenv.pypa.io/en/stable/) in order to avoid installing the packages globally.
```
$ pip install -r requirements.txt
```

#### Install frontend dependencies
```
$ npm install
$ grunt
```

### Setup the database
Before anything, you must apply the Django migrations:
```
python manage.py migrate
```

Optionally, you can pre-populate the database with examples:
```
$ python populate.py
``` 

### Running the server
You can run the server by running the command below:
```
$ python manage.py runserver
```
The app should be running at http://127.0.0.1:8000.
