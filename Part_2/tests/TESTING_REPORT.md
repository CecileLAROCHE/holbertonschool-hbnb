# Curl Test

1. Users
2. Amenities
3. Places
4. Revieuw

## 1. Users

**Endpoint:** POST /api/v1/users/

### Create user

`curl -X POST "http://127.0.0.1:5000/api/v1/users/"
-H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/T6_create_user.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/T6_create%20user_.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Duplicate Email

`curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_duplicate_email.png?raw=true" alt="duplicate_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_duplicate_email_.png?raw=true" alt="duplicate_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Invalid name

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_unvalid_name.png?raw=true" alt="unvalid_name" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_unvalid_name_.png?raw=true" alt="unvalid_name" width="900"><!-- markdownlint-disable-line MD033 --></p>

### Invalid email

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_unvalid_email.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part_2/Picture_for_README/t6_unvalid_email_.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

## 2. Amenities

## 3. Places

## 4. Revieuw
