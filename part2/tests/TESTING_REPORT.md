# Test

## pytest

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/pytest.png?raw=true" alt="pytest" width="900"><!-- markdownlint-disable-line MD033 --></p>

## Swagger

Here, you can find the Swagger's documentation :

`http://127.0.0.1:5000/api/v1/`\

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/Documentation-Swagger.png?raw=true" alt="pytest" width="900"><!-- markdownlint-disable-line MD033 --></p>

## Curl Test

Below, a series of test examples carried out in curl

1. [Users](#1-users)  
2. [Amenities](#2-amenities)  
3. [Places](#3-places)  
4. [Review](#4-review)

### 1. Users

**Endpoint:** POST /api/v1/users/

#### Create user

`curl -X POST "http://127.0.0.1:5000/api/v1/users/"
-H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/T6_create_user.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/T6_create%20user_.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Duplicate Email

`curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_duplicate_email.png?raw=true" alt="duplicate_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_duplicate_email_.png?raw=true" alt="duplicate_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Invalid name

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_unvalid_name.png?raw=true" alt="unvalid_name" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_unvalid_name_.png?raw=true" alt="unvalid_name" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### Invalid email

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_unvalid_email.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_unvalid_email_.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### List of users

`curl -X GET http://localhost:5000/api/v1/users/`

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_list_users.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_list_users_.png?raw=true" alt="create_user" width="900"><!-- markdownlint-disable-line MD033 --></p>

### 2. Amenities

#### Create Amenity

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_create_amenity.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_create_amenity_.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

#### List Amenities

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_list_amenities.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_list_amenities_.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

### 3. Places

#### Create

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_create_place.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/t6_create_place_.png?raw=true" alt="" width="900"><!-- markdownlint-disable-line MD033 --></p>

### 4. Review

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/part2/Picture_for_documentation/create_review.png?raw=true" alt="create_revieux" width="900"><!-- markdownlint-disable-line MD033 --></p>
