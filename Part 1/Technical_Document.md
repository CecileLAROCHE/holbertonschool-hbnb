# Technical Document

## Introduction

This document is a compilation of the 3 types of diagrams asked at the beginning of a project

1 - [High-Level Diagrams](#high-level-architecture)
2 - [Business Logic Layer](#business-logic-layer)
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
* He send request tothe app HBnB.
* He can be an administrator ot not.

**Presentation Layer**
This layer contain 2 items
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

Objective : Design a detailed class diagram for the Business Logic layer of the HBnB application. This diagram will depict the entities within this layer, their attributes, methods, and the relationships between them. The primary goal is to provide a clear and detailed visual representation of the core business logic, focusing on the key entities: User, Place, Review, and Amenity.

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Class%20Diagram.png?raw=true" alt="Class-diagram" width="500"><!-- markdownlint-disable-line MD033 --></p>

## API Interaction Flow

Objective : Develop sequence diagrams for at least four different API calls to illustrate the interaction between the layers (Presentation, Business Logic, Persistence) and the flow of information within the HBnB application. The sequence diagrams will help visualize how different components of the system interact to fulfill specific use cases, showing the step-by-step process of handling API requests.

### User Registration

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_User%20Registration.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

### Place Creation

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Place%20Creation.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

### Review Submission

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Review%20Submission.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>

## Fetching a List of Places

<p align="center"><img src="https://github.com/CecileLAROCHE/holbertonschool-hbnb/blob/main/Part%201/Diagram%20pictures/Sequence%20Diagrams_Fetching%20a%20List%20of%20Places%20diagram.png?raw=true" alt="High-Level" width="800"><!-- markdownlint-disable-line MD033 --></p>
