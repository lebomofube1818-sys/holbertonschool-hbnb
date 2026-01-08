# HBnB Technical Documentation

## Introduction
This document provides a technical overview of the HBnB application architecture. It consolidates diagrams and explanations to guide implementation.

---

## High-Level Architecture

The HBnB system follows a layered architecture to separate concerns and improve maintainability.

```mermaid
classDiagram
class PresentationLayer
class BusinessLogicLayer
class PersistenceLayer

PresentationLayer --> BusinessLogicLayer : uses
BusinessLogicLayer --> PersistenceLayer : persists

Explanation

Presentation Layer handles API requests.

Business Logic Layer contains core application rules.

Persistence Layer manages data storage.

Business Logic Layer

The Business Logic layer defines the core entities of the system.

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
}

class Review {
    UUID id
    int rating
    string comment
    datetime created_at
    datetime updated_at
}

class Amenity {
    UUID id
    string name
    string description
    datetime created_at
    datetime updated_at
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has

Entity Descriptions

User: Represents a system user.

Place: Represents a listed property.

Review: Represents feedback on a place.

Amenity: Represents features associated with places.

API Interaction Flow

sequenceDiagram
Client ->> API: GET /places
API ->> BusinessLogic: fetch_places()
BusinessLogic ->> Persistence: query_places()
Persistence -->> BusinessLogic: places
BusinessLogic -->> API: places
API -->> Client: response

Explanation
This sequence shows how a request flows through the system layers

Conclusion
This document serves as a reference for understanding the HBnB system architecture and design.
