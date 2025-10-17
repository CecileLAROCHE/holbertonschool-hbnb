# README of the project HBnH - BL and API

![Project Status](https://img.shields.io/badge/status-development-yellow)  ![License: Edu](https://img.shields.io/badge/license-Educational-lightgrey)  ![buil with](https://img.shields.io/badge/built_with-❤️‍🔥-df0000)\
![GitHub last commit](https://img.shields.io/github/last-commit/CecileLAROCHE/holbertonschool-hbnb?label=Last%20commit)

<p align="center"><img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3lsbHE5ZTV6dnFzZXg1ZnVhZTIwaWFyMzd2bzlqaWZrMHY2b2JjcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1hBWHsBYoqYOfsmAsL/giphy.gif" alt="fire" width="300"><!-- markdownlint-disable-line MD033 --></p>

## 📖 Description

This part 2 of the project HBnB is about Implementation of Business Logic and API Endpoints

## 🧭 Index

1 - [⚙️ Cloning and Compilation](#️-cloning-and-compilation)\
2 - [🚀 Features / Limitations](#-features--limitations)\
3 - [📚 Files in Repository](#-files-in-repository)\
4 - [🧪 Tests and outputs](#-tests-and-outputs)\
5 - [📁 Project Structure](#-project-structure)\
6 - [👥 Author](#-author)\
7 - [📜 License](#-license)

## ⚙️ Cloning and Compilation

### ✅ Prerequisites

**GCC** installed on your system.\
**Ubuntu 20.04 LTS** (or equivalent).

### 📥 Clone

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo` | `git clone https://github.com/CecileLAROCHE/holbertonschool-hbnb.git` |

### virtual environment

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Create virtual environment:` | `python3 -m venv venv` |
| `activate virtual environment:` | `source venv/bin/activate` |
| `Install dependencies:` | `pip install -r requirements.txt` |
| `deactivate virtual environment:` | `deactivate` |

### Install dependencies

| Task |Command|
|--------------------------------------------|-------------------------------------------------------
| `Install dependencies:` | `pip install -r requirements.txt` |

### Run the application

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo:` | `git clone https://github.com/CecileLAROCHE/holbertonschool-hbnb.git` |
| `Run:` | `python3 -m run` |

## 🚀 Features / Limitations

### ✅ Features

* Create User, Amenity, Place and Review
* Tests User, Amenety and Place

### ⚠️ Limitations

* no passworld management
* no administrator management
* no delete option
* no test for Review

## 🧪 Tests and Outputs

Verifying the creation of models :

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Business_Logic_Classes.png?raw=true" alt="blc" width="900"><!-- markdownlint-disable-line MD033 --></p>

The test for the task 6 are here :

* [TESTING_REPORT.md](https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/tests/TESTING_REPORT.md)

### User Endpoints

#### Create a user

`curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "Jane",
    "last_name": "Do",
    "email": "Jane.DO@example.com"
}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Create_user.png?raw=true" alt="create" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Email already registered

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Error_email_exist.png?raw=true" alt="already" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Get a user by ID

`curl -X GET http://localhost:5000/api/v1/users/<user_id>`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Get_a_user_by_ID.png?raw=true" alt="get" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### List all users

`curl -X GET http://localhost:5000/api/v1/users/`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Get_a_user_by_ID.png?raw=true" alt="list" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Update a user

`curl -X PUT http://localhost:5000/api/v1/users/<user_id>
-H "Content-Type: application/json"
-d '{"first_name": "Jane", "last_name": "Smith-Do", "email": "Jane.Smith-Do@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Update_a_user.png?raw=true" alt="update" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Amenity Endpoints

#### Create Amenity

`curl -X POST http://localhost:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Create_amenity.png?raw=true" alt="create_amenity" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Place Endpoints

#### Create Place

`curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{
  "title": "Villa Sunset",
  "description": "Belle villa avec vue sur la mer",
  "price": 250.0,
  "latitude": 43.2965,
  "longitude": 5.3698,
  "owner_id": "<user_id>"
}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/create_place.png?raw=true" alt="create_place" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Review Endpoints

#### Create Revieuw

`curl -X POST http://localhost:5000/api/v1/reviews/
-H "Content-Type: application/json"
-d '{
  "text": "Super séjour !",
  "rating": 5,
  "user_id": "<user_id>",
  "place_id": "<place_id>"
}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/create_place.png?raw=true" alt="create_revieux" width="900"><!-- markdownlint-disable-line MD033 --></p>

## 📁 Project Structure

tree -I "**pycache**|*.pyc|.git"

├── Part 2\
│   ├── app\
│   │   ├── api\
│   │   │   └── v1\
│   │   │       ├── amenities.py\
│   │   │       ├── \_\_init\_\_.py\
│   │   │       ├── places.py\
│   │   │       ├── reviews.py\
│   │   │       └── users.py\
│   │   ├── \_\_init\_\_.py\
│   │   ├── models\
│   │   │   ├── amenity.py\
│   │   │   ├── \_\_init\_\_.py\
│   │   │   ├── place.py\
│   │   │   ├── review.py\
│   │   │   └── user.py\
│   │   ├── persistence\
│   │   │   ├── \_\_init\_\_.py\
│   │   │   └── repository.py\
│   │   └── services\
│   │       ├── facade.py\
│   │       └── \_\_init\_\_.py\
│   ├── tests\
│   │   ├── \_\_init\_\_.py\
│   │   ├── test_amenities\
│   │   ├── test_base-model\
│   │   ├── test_Place\
│   │   ├── test_reviews\
│   │   ├── test_users\
│   │   ├──TESTING_REPORT\
│   ├── config.py\
│   ├── README.md\
│   ├── requirements.txt\
│   └── run.py\
└── README.md

## 👥 Author

This project was developed by Holberton student as a programming exercise.\
\
**Cécile LAROCHE** [GitHub](https://github.com/CecileLAROCHE)

## 📜 License

This project is for educational purposes only as part of Holberton School.
