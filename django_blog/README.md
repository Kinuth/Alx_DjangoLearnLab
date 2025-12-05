# Django Blog Project

A multi-user blogging platform built with Django.

## Features
* **User Authentication:** Users can register, login, and logout.
* **CRUD Operations:** Users can Create, Read, Update, and Delete posts.
* **Permissions:** * Users can only update/delete their own posts.
    * Posts are publicly readable.

## How to Run
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run migrations: `python manage.py migrate`
4.  Start server: `python manage.py runserver`

## Data Handling
* **Author Assignment:** The `author` field is automatically populated based on the `request.user` session during post creation.