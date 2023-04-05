# Project name:  Little lemon restaurant API

![MasterHead](https://www.48hourslogo.com/oss/works/2022/01/12/135536140395/115168_45900_7388b824-b2f0-4ffa-ae56-58d13a637de8.jpg)

## Project description
This is a backend project for a restaurant service which provides API endpoints for User interface to interact with.

## Features

1.	The admin can assign users to the manager group

2.	You can access the manager group with an admin token

3.	The admin can add menu items 

4.	The admin can add categories

5.	Managers can log in 

6.	Managers can update the item of the day

7.	Managers can assign users to the delivery crew

8.	Managers can assign orders to the delivery crew

9.	The delivery crew can access orders assigned to them

10.	The delivery crew can update an order as delivered

11.	Customers can register

12.	Customers can log in using their username and password and get access tokens

13.	Customers can browse all categories 

14.	Customers can browse all the menu items at once

15.	Customers can browse menu items by category

16.	Customers can paginate menu items

17.	Customers can sort menu items by price

18.	Customers can add menu items to the cart

19.	Customers can access previously added items in the cart

20.	Customers can place orders

21.	Customers can browse their own orders

## Setting up the Backend

### Install Dependencies

1. **Python 3.10** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

- Python 3.10 upward is required

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup cd into the project directory and run the commands below:

- **Start and activate your virtual environment**

```bash
# Mac and Linux users

python3 -m venv env
source env/bin/activate

# Windows users
> py -3 -m venv env
> env\Scripts\activate

# Windows git bash users
python3 -m venv env
source env/bin/activate
```

Run This command to install the required project dependencies e.g Django

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Django](https://www.djangoproject.com/) Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

### Set up the Database

```bash
python manage.py makemigrations
python manage.py migrate

```

### Run the Server

After successfully setting up and installing the dependencies and setting up the Database start your backend Django server by running the command below from the root of the directory (where the manage.py file is located).

```bash
python manage.py runserver
```

## Author

Akinola Samson <akinolasamson1234@gmail.com>