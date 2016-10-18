# Swapp

## Description

Project developped at HEIG-VD in the PDG course by a team of 5 people. 

It consists in a web app on which an user can trade objects with other people.

## Installation

### Prerequisites
Python 3.5

### Installation steps
Begin by cloning the repo:
```
git clone git@github.com:Flagoul/swapp.git
```
Optional: create a virtualenv: 
```
cd /HEIG_PDG_2016/
virtualenv env
source ./env/Scripts/activate
```
Install dependencies:
```
pip install -r requirements.txt
```

Finally, start the server:
```
python manage.py runserver
```
The app should be running at http://127.0.0.1:8000.
