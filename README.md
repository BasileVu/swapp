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
> git clone git@github.com:Flagoul/swapp.git
```
Optional: create a virtualenv: 
```
> cd /HEIG_PDG_2016/
> virtualenv env
> source ./env/Scripts/activate
```
#### Install backend dependencies :
```
> pip install -r requirements.txt
```
#### Install frontend dependencies :
install sass :
http://sass-lang.com/install

To install sass you must first download the ruby installer from http://rubyinstaller.org/

Then you must run this command and accept the certificate (on windows).

```
gem source -a http://rubygems.org/
```

Then install sass with 

```
gem install sass
```

Finally you can install the dependencies in the project with :

```
> npm install
> grunt
```

Finally, start the server:
```
> python manage.py runserver
```
The app should be running at http://127.0.0.1:8000.

Optionally, you can set the server to watch your development changes using :
```
> grunt watch
```
