# HBnB – Technical Documentation (Part 1)

## Introduction
This document provides the technical documentation for the HBnB Evolution application.
It describes the system architecture, the business logic design, and the interactions
between components. This documentation serves as a blueprint for the implementation
phases of the project.

---

## High-Level Architecture

```mermaid
classDiagram
class PresentationLayer
class BusinessLogicLayer
class PersistenceLayer

PresentationLayer --> BusinessLogicLayer : Facade
BusinessLogicLayer --> PersistenceLayer : Data Access

Explanation

Presentation Layer: Handles API endpoints and user interactions.

Business Logic Layer: Contains core application rules and models.

Persistence Layer: Manages database storage and retrieval.

The Facade pattern simplifies communication between layers.

Business Logic Layer – Class Diagram

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

Explanation

User: Represents system users (regular or admin). Can own Places and write Reviews.

Place: Represents properties owned by Users. Can have Reviews and Amenities.

Review: Represents feedback left by Users for Places.

Amenity: Represents features associated with Places.

Relationships:

User “1” → Place “0..*” : owns

User “1” → Review “0..*” : writes

Place “1” → Review “0..*” : receives

Place “0..” → Amenity “0..” : has

API Interaction Flow

sequenceDiagram
Client ->> API: GET /places
API ->> BusinessLogic: fetch_places()
BusinessLogic ->> Persistence: query_places()
Persistence -->> BusinessLogic: places
BusinessLogic -->> API: places
API -->> Client: response

Explanation

This sequence shows how a request flows through the system layers from Client → API → Business Logic → Persistence → back.

Conclusion

This document outlines the architectural structure and business logic of the HBnB application.
The diagrams and explanations together provide a clear reference for implementation phases.
