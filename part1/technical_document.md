# HBnB Technical Documentation

---

## Introduction

The purpose of this document is to provide a comprehensive technical blueprint for the HBnB project.  
It consolidates all architecture and design diagrams, along with explanatory notes, to guide the implementation phase and serve as a reference for developers.

This document covers:

- High-Level Architecture (Package Diagram)  
- Business Logic Layer (Class Diagram)  
- API Interaction Flow (Sequence Diagrams)  

---

## High-Level Architecture

### Layered Architecture Overview

The HBnB application uses a three-layer architecture:

1. **Presentation Layer**: Handles user interactions via API and services.  
2. **Business Logic Layer**: Contains the core models representing entities like User, Place, Review, and Amenity.  
3. **Persistence Layer**: Responsible for data storage and retrieval from the database.  

The **Facade Pattern** is used to simplify communication between layers by providing a unified interface.

### High-Level Package Diagram

```mermaid
classDiagram
class API
class Services
class Facade
class User
class Place
class Review
class Amenity
class Repository
class Database

API --> Facade : <<facade>>
Facade --> Repository : data access
```
Notes:

Shows the three-layer architecture

API and Services interact with Business Logic through the Facade

Repository communicates with Database for persistence

## Detailed Class Diagram
```mermaid
classDiagram
class User {
    +UUID id
    +String name
    +String email
    +create()
    +update()
}
class Place {
    +UUID id
    +String title
    +String description
    +create()
    +update()
}
class Review {
    +UUID id
    +String text
    +create()
    +update()
}
class Amenity {
    +UUID id
    +String name
    +create()
    +update()
}

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "*" --> "*" Amenity : has
```
Notes:

Each entity has a unique identifier (UUID) and timestamps (creation & update)

Relationships:

 -User can own multiple Places and write multiple Reviews

 -Place can have multiple Reviews and Amenities

This diagram captures the core business logic

## API Interaction Flow

**User Registration**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /users (signup data)
API->>BusinessLogic: validate user data
BusinessLogic->>Database: create new User record
Database-->>BusinessLogic: return success
BusinessLogic-->>API: return user info
API-->>User: 201 Created / success message
```

Notes:

User data flows from API → BusinessLogic → Database

New user is created successfully

**Place Creation**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /places (new place data)
API->>BusinessLogic: validate place data
BusinessLogic->>Database: save Place record
Database-->>BusinessLogic: confirmation saved
BusinessLogic-->>API: return place info
API-->>User: 201 Created / place details
```

Notes:

Adds a new rental listing

Validation and persistence handled by BusinessLogic and Database

**Review Submission**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /reviews (review text, place_id)
API->>BusinessLogic: validate review & user_id
BusinessLogic->>Database: save Review record
Database-->>BusinessLogic: confirmation saved
BusinessLogic-->>API: return review info
API-->>User: 201 Created / review details
```

Notes:

User submits a review for a place

Review linked to both User & Place

**Fetching a List of Places**
```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: GET /places (optional filters)
API->>BusinessLogic: query places with filters
BusinessLogic->>Database: retrieve matching Place records
Database-->>BusinessLogic: return place list
BusinessLogic-->>API: return place list
API-->>User: 200 OK / list of places
```

Notes:

Shows data retrieval flow

Includes optional filtering logic in BusinessLogic
--
## Conclusion

This document provides a complete reference for the HBnB project’s architecture and design.
It captures the high-level package structure, detailed business logic, and API interaction flows, serving as a guide for development and future maintenance.
