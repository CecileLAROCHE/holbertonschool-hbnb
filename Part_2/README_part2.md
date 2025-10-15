# README of the project HBnH - BL and API

![Project Status](https://img.shields.io/badge/status-development-yellow)  ![License: Edu](https://img.shields.io/badge/license-Educational-lightgrey)  ![buil with](https://img.shields.io/badge/built_with-❤️‍🔥-df0000)\
![GitHub last commit](https://img.shields.io/github/last-commit/CecileLAROCHE/holbertonschool-hbnb?label=Last%20commit)

<p align="center"><img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExb3lsbHE5ZTV6dnFzZXg1ZnVhZTIwaWFyMzd2bzlqaWZrMHY2b2JjcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1hBWHsBYoqYOfsmAsL/giphy.gif" alt="fire" width="300"><!-- markdownlint-disable-line MD033 --></p>

## 📖 Description

this part

## 🧭 Index

1 - [⚙️ Cloning and Compilation](#️-cloning-and-compilation)\
2 - [🚀 Features / Limitations](#-features--limitations)\
3 - [📚 Files in Repository](#-files-in-repository)\
4 - [📄 Man Page](#-man-page)\
5 - [🧪 Tests and outputs](#-tests-and-outputs)\
6 - [📁 Project Structure](#-project-structure)\
7 - [👥 Author](#-author)\
8 - [📜 License](#-license)

## ⚙️ Cloning and Compilation

### ✅ Prerequisites

**GCC** installed on your system.\
**Ubuntu 20.04 LTS** (or equivalent).

### 📥 Clone

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo` | `git clone https://github.com/CecileLAROCHE/holbertonschool-hbnb.git` |

### Install dependencies

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Create virtual environment:` | `python3 -m venv venv` |
| `activate virtual environment:` | `source venv/bin/activate` |
| `Install dependencies:` | `pip install -r requirements.txt` |

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `install flask-restx:` | `pip install flask-restx` |

pip install flask-restx

### Run the application

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo:` | `git clone https://github.com/CecileLAROCHE/holbertonschool-hbnb.git` |
| `Run:` | `python3 -m run` |

## 🚀 Features / Limitations

### ✅ Features

* in progress
*
*
*

### ⚠️ Limitations

* in progress

## 📚 Files in Repository

### 🖥️ Source Code Files

| File                   | Description                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| `none`              | . |
| ``              | . |

### 📑 Documentation Files

| File                 | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `` | '' |

## 📋 Man page

`to do``

## 🧪 Tests and Outputs

`to do`

### User Endpoints

#### Create a user

`curl -X POST http://localhost:5000/api/v1/users/
     -H "Content-Type: application/json"
     -d '{"first_name": "Jane", "last_name": "Do", "email": "Jane.Do@example.com"}'`

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

`curl -X PUT http://localhost:5000/api/v1/users/9856e862-8d67-43aa-a8ca-804197bc2698
-H "Content-Type: application/json"
-d '{"first_name": "Jane", "last_name": "Smith-Do", "email": "Jane.Smith-Do@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/Update_a_user.png?raw=true" alt="update" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Amenity Endpoints

#### Create Amenity

`curl -X POST http://localhost:5000/api/v1/amenities/ -H "Content-Type: application/json" -d '{"name": "Wi-Fi"}'`

### Place Endpoints

#### Create Place

`curl -X POST http://localhost:5000/api/v1/places/ -H "Content-Type: application/json" -d '{
  "title": "Villa Sunset",
  "description": "Belle villa avec vue sur la mer",
  "price": 250.0,
  "latitude": 43.2965,
  "longitude": 5.3698,
  "owner_id": "b6b36360-6488-4004-b7dd-85f15ec6f557"
}'`

### Review Endpoints

#### Create REvieuw

`curl -X POST http://localhost:5000/api/v1/reviews/
-H "Content-Type: application/json"
-d '{
  "text": "Super séjour !",
  "rating": 5,
  "user_id": "0f78390b-a75d-4a05-8ec0-3d94b92a6879",
  "place_id": "ea42e76c-7168-408f-b31c-5008604b7640"
}'`

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
