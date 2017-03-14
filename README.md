# Swapp
[![Build Status](https://travis-ci.com/Flagoul/swapp.svg?token=EpMgztqGsgqLdu8HDosP&branch=master)](https://travis-ci.com/Flagoul/swapp)

## Description
A project developped at HEIG-VD in the PDG course in a team of 5 people.

It consists in a web platform on which users can trade objects. Various filters are provided to find objects, such as object proximity, price range, categories and so on.

## Contributing
### Prerequisites
* Python 3.5
* npm 3.5
* sass 3.4.23

### Installation steps
Begin by cloning the repo and go into it:
```
$ git clone git@github.com:Flagoul/swapp.git
$ cd swapp
```
#### Install backend dependencies :
Before running the command below, you may want to setup a [virtualenv](https://virtualenv.pypa.io/en/stable/) in order to avoid installing the packages globally.
```
$ pip install -r requirements.txt
```

#### Install frontend dependencies :
```
$ npm install
$ grunt
```

Finally, you can start the server:
```
$ python manage.py runserver
```

The app should be running at http://127.0.0.1:8000.

Optionally, you can set the server to watch your development changes using:
```
$ grunt watch
```

## Authors
This project was built by [Sébastien Boson](https://github.com/sebastie-boson), [Antoine Drabble](https://github.com/servietsky777), [Sébastien Richoz](https://github.com/sebastienrichoz), [Mathieu Urstein](https://github.com/MathieuUrstein) and [Basile Vu](https://github.com/Flagoul). 
