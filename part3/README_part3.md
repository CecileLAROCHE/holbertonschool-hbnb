# README of the project HBnB - Auth & DB

![Project Status](https://img.shields.io/badge/status-development-yellow)  ![License: Edu](https://img.shields.io/badge/license-Educational-lightgrey)  ![buil with](https://img.shields.io/badge/built_with-❤️‍🔥-df0000)\
![GitHub last commit](https://img.shields.io/github/last-commit/CecileLAROCHE/holbertonschool-hbnb?label=Last%20commit)

<p align="center"><img src="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExN3k2cWRwYWl6cGFmYzFocDAxOW5zdDd3d3N0MThwbG9iMTE4eDJ3aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26BROFLJSFhP0cMGk/giphy.gif" alt="password" width="600"><!-- markdownlint-disable-line MD033 --></p>

## 📖 Description

T

## 🧭 Index

1 - [⚙️ Cloning and Compilation](#️-cloning-and-compilation)\
2 - [🚀 Features / Limitations](#-features--limitations)\
3 - [📚 Files in Repository](#-files-in-repository)\
4 - [📄 Man Page](#-man-page)\
5 - [🧪 Tests and outputs](#-tests-and-outputs)\
6 - [📁 Project Structure](#-project-structure)\
7 - [👥 Authors](#-authors)\
8 - [📜 License](#-license)

## ⚙️ Cloning and Compilation

### ✅ Prerequisites

**GCC** installed on your system.\
**Ubuntu 20.04 LTS** (or equivalent).

### 📥 Clone and execution

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Clone repo` | `git clone https://github.com/CecileLAROCHE/holbertonschool-hbnb.git` |

### virtual environment

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Create virtual environment:` | `python3 -m venv venv` |
| `activate virtual environment:` | `source venv/bin/activate` |
| `deactivate virtual environment:` | `deactivate` |

### Install dependencies

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Install dependencies:` | `pip install -r requirements.txt` |

### Run the application

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Run:` | `python3 -m run` |

### First run

| Task |Command|
|--------------------------------------------|-------------------------------------------------------|
| `Run flask:` | `flask shell` |
| `Create all tables:` | `from app import db`<br>`db.create_all()`|
| `Check:` | `from app.models.user import User`<br>`User.query.all()`|
| `Exit:` | `exit()` |

## 🚀 Features / Limitations

### ✅ Features

*
*
*
*

### ⚠️ Limitations

*

## 📚 Files in Repository

### 🖥️ Source Code Files

| File                   | Description                                                                                         |
| ---------------------- | --------------------------------------------------------------------------------------------------- |
| `none`              | . |
| ``              | . |

### 📑 Documentation Files

| File                 | Description                                                       |
| -------------------- | ----------------------------------------------------------------- |
| `` |   |

## 📋 Man page

`to do`

## 🧪 Tests and Outputs

`to do`

## 📁 Project Structure

tree -I "**pycache**|*.pyc|.git"

To have more details, please go see the README of each part

├── app
│   ├── api
│   │   ├── \_\_init\_\_.py.py
│   │   └── v1
│   ├── \_\_init\_\_.py.py
│   ├── models
│   │   ├── amenity.py
│   │   ├── basemodel.py
│   │   ├── \_\_init\_\_.py.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence
│   │   ├── amenity_repository.py
│   │   ├── database.py
│   │   ├── \_\_init\_\_.py.py
│   │   ├── place_repository.py
│   │   ├── repository.py
│   │   ├── review_repository.py
│   │   └── user_repository.py
│   ├── services
│   │   ├── facade.py
│   │   └── \_\_init\_\_.py.py
│   └── tests
│       ├── conftest.py
│       ├── \_\_init\_\_.py.py
│       ├── test_amenity.py
│       ├── test_place.py
│       ├── test_review.py
│       └── test_user.py
├── config.py
├── create_admin.py
├── hbnb.db
├── instance
│   └── development.db
├── pyvenv.cfg
├── README_part3.md
├── requirements.txt
└── run.py

## 👥 Authors

This project was developed by Holberton student as a programming exercise.\
\
**Cécile LAROCHE** [GitHub](https://github.com/CecileLAROCHE)

## 📜 License

This project is for educational purposes only as part of Holberton School.
