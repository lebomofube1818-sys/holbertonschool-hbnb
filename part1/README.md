# HBnB – Technical Architecture Documentation

## Introduction
This document provides a comprehensive technical overview of the HBnB project. It consolidates architectural diagrams and explanatory notes to guide development and ensure a clear understanding of the system design.

---

## High-Level Architecture

The HBnB application follows a layered architecture pattern. This separation improves scalability, testability, and maintainability.

### High-Level Package Diagram

```mermaid
classDiagram
class PresentationLayer
class BusinessLogicLayer
class PersistenceLayer

PresentationLayer --> BusinessLogicLayer : uses
BusinessLogicLayer --> PersistenceLayer : persists
Explanation

The Presentation Layer handles API requests.

The Business Logic Layer contains core domain logic.

The Persistence Layer manages data storage.

Business Logic Layer
This layer contains the core entities of the HBnB application.

Detailed Class Diagram
mermaid
Copy code
classDiagram
class User {
    UUID id
    string first_name
    string last_name
    string email
    string password
    boolean is_admin
    datetime created_at
    datetime updated_at

    create()
    update()
    delete()
}

class Place {
    UUID id
    string title
    string description
    float price
    float latitude
    float longitude
    datetime created_at
    datetime updated_at

    create()
    update()
    delete()
}

class Review {
    UUID id
    int rating
    string comment
    datetime created_at
    datetime updated_at

    create()
    update()
    delete()
}

class Amenity {
    UUID id
    string name
    string description
    datetime created_at
    datetime updated_at

    create()
    update()
    delete()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has
Entity Descriptions
User
Represents a platform user. Users can own places and write reviews.

Place
Represents a listed property. Each place belongs to one user.

Review
Represents feedback left by a user on a place.

Amenity
Represents features associated with places.

API Interaction Flow
The following sequence demonstrates how a client retrieves places.

mermaid
Copy code
sequenceDiagram
Client ->> API: GET /places
API ->> BusinessLogic: fetch_places()
BusinessLogic ->> Persistence: query_places()
Persistence -->> BusinessLogic: places
BusinessLogic -->> API: places
API -->> Client: response
Explanation
This flow shows how data moves through the system layers when retrieving places.

Conclusion
This document serves as a blueprint for the HBnB system architecture and will guide implementation and maintenance.
