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

User represents system users (regular or admin).

Place represents properties owned by users.

Review represents feedback left by users for places.

Amenity represents features associated with places.

Relationships define ownership, reviews, and amenities.

Conclusion

This document outlines the architectural structure and business logic of the HBnB
application. The diagrams and explanations together provide a clear reference
for future implementation phases.
