# Technical Document

## Introduction

This document is a compilation of the 3 types of diagrams asked at the beginning of a project

1 - [High-Level Diagrams](#high-level-architecture)\
2 - [Business Logic Layer](#business-logic-layer)\
3 - [API Interaction Flow](#api-interaction-flow)

## High-Level Architecture

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/High-Level%20Diagram.png?raw=true" alt="High-Level" width="150"><!-- markdownlint-disable-line MD033 --></p>

This diagram provide a conceptual overview of how the different components of the application are organized and how they interact with each other.
This high-level package diagram that illustrates the three-layer architecture of the HBnB application and the communication between these layers via the facade pattern.
Below, there are the most important point of this diagram

**User**

* He is the who have interacction with apps, like:
  * create a place
  * let a review
  * check place.
* He send request to the app HBnB.
* He can be an administrator ot not.

**Presentation Layer**\
This layer contain 2 items\
***API***

* Receive request from user
* Transmit request to next step

***API Endpoints***

* Sent request to the good layer for execute

**Business Logic Layer / Façade Pattern**

* This layer contain 4 items:
  * User
  * Place
  * Review
  * Amenity
* All business activity is in this layer
* Interactions between the different items will be defined later

**Persistence Layer**

* This layer contain 2 items
  * Data Storage
  * data access
* This layer manage the data

**Data base**

* This is the place where all the data are save in security

## Business Logic Layer

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Class%20Diagram.png?raw=true" alt="Class-diagram" width="500"><!-- markdownlint-disable-line MD033 --></p>

This diagram depict the entities within this layer, their attributes, methods, and the relationships between them. The goal is to provide a clear and detailed visual representation of the core business logic, focusing on the key entities: User, Place, Review, and Amenity.

**BaseModel**\
This class is an abstract class. all the items which are in is needeed for all the others class.\
***attributes:*** id, create_at, usdate_at, delete_at\
***methods:*** save(), delete()

**User**\
This class is for people, they can be owner or renter\
***attributes:*** firstname, lastname, email, password\
***methods:*** verify_email, hash_password, verify_password

**Place**\
This class is for the details of the place to rent\
***attributes:*** tittle, description, price, latitude, longitude\
***methods:*** add_review, get_average, add_amenity

**Amenity**\
This class is for all the amenity able for a place\
***attributes:*** name, description\
***methods:*** is_avaible, get_info, get_summarry

**Review**\
This class is for the revieux of the rent\
***attributes:*** rating, comment, language, revieux_date\
***methods:*** is_valid, reprt_innappropriate

### Link

* User, Place, Amenity and Review are children of BaseModel
* User can own many Place, but each Place has 1 owning User.
* User can write many Review, but each Review belongs to 1 User.
* Place can have many Review, but each Review belongs to 1 Place.
* Place can have many Amenity, and an Amenity can be linked to many Place.

## API Interaction Flow

This 4 sequence diagrams help to visualize how different components of the system interact to fulfill specific use cases, showing the step-by-step process of handling API requests.

### User Registration

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_User%20Registration.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

This diagram show the step the program will do to register a new user.

**Steps**
➡ API call\
↩ return if unvalid data\
  ➡ process request\
    ➡ Save data\
    🔙 confirm save\
  🔙 return response\
🔙 return success

### Place Creation

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Place%20Creation.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

This diagram show the step the program will do to create a new Plave.

**Steps**
➡ forme registration\
↩ return if unvalid data\
  ➡ Create place\
  ↩ Return error\
    ➡ Save place\
    🔙 Place saved\
  🔙 return\
🔙 return create

### Review Submission

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Review%20Submission.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

This diagram show the step the program will do to submit a new review.

**Steps**
➡ forme registration\
↩ return if unvalid data\
  ➡ Create review\
  ↩ Return error\
    ➡ Save revieux\
    🔙 Review saved\
  🔙 return\
🔙 return create

## Fetching a List of Places

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Fetching%20a%20List%20of%20Places%20diagram.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

This diagram show the step the program will do to fetching a List of Places.

**Steps**
➡ Filter\
↩ return if bad request\
  ➡ validate filter\
  ↩ unvalidate filter\
    ➡ select place\
    🔙 list\
  🔙 return list\
🔙 return list
