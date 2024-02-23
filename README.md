# Presentation Digikala
The purpose of this project is to make a presentation for a manager or employee of _Digikala_, who can use it in meetings.

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/KarYar-ToTheSun/backend.git
$ cd backend
```
Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv env
$ source env/bin/activate
```
Then install the dependencies:

```sh
(env)$ pip install -r requirements/base.txt
(env)$ pip install -r requirements/local.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```

## apps
In our project, we have four apps named `user`, `presentation`, `slide`, and `digiKala`

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## utils
### create_code.py
- This file was created to create a 258 character code to verify the user account and the `activision_code` field.
### data_digikala.py
- This file was created to get data from the digital product link ('URL_DIGIKAL'), such as getting the information of the chapters and sections of a chapter and getting the sections of a chapter with the link that the user enters.
### tags.py
- This file was created to handle issues related to the tag field in the presentation model, such as creating a tag and deleting and returning the names of the created tags, and the tags are deleted that are not related to the presentation .
### data_presentation.py
- This file was created to avoid repeating the code and it is used in `PresentationView` and `PresentationBySlugView` in the `presentation app` in `views.py` file.

## Diagram Sql Projects
![diagram_sql](https://github.com/KarYar-ToTheSun/backend/blob/master/diagram_sql/diagram_models.png)
