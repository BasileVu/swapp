# Swapp

[![Build Status](https://travis-ci.com/Flagoul/swapp.svg?token=EpMgztqGsgqLdu8HDosP&branch=master)](https://travis-ci.com/Flagoul/swapp)

## Description

A project developped at HEIG-VD in the PDG course in a team of 5 people:
[Sébastien Boson](https://github.com/sebastie-boson), [Antoine Drabble](https://github.com/servietsky777), [Sébastien Richoz](https://github.com/sebastienrichoz), [Mathieu Urstein](https://github.com/MathieuUrstein) and [Basile Vu](https://github.com/Flagoul).

It consists in a web platform on which users can trade objects. Various filters are provided to find objects, such as object proximity, price range, categories and so on.

### Overview 
![home](https://user-images.githubusercontent.com/2306585/31589874-b4b3dd16-b208-11e7-9026-9da8d014e863.jpg)
*The home page with popular tradable items*


![item-1](https://user-images.githubusercontent.com/2306585/31589959-a4c65856-b209-11e7-8674-cd0c40280c0a.jpg)
![item-2](https://user-images.githubusercontent.com/2306585/31589993-ed00703e-b209-11e7-86e1-25426581c9fe.png)
*Overview of an item with its various details and possible interactions*


![swapp2](https://user-images.githubusercontent.com/2306585/31590032-3aa2a3e8-b20a-11e7-8aa7-1579a2327172.png)
*Preview of a swap proposition*


![search-advanced](https://user-images.githubusercontent.com/2306585/31590041-6bdd8b8a-b20a-11e7-8a64-8758c818ee05.jpg)
*Various search filters can be applied, with advanced filters such as distance and/or price ranges*

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
