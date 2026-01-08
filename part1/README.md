# HBnB Technical Documentation

## Introduction

This document provides a comprehensive technical overview of the HBnB project.  
It consolidates all architectural and design diagrams created during the analysis phase and serves as a reference guide for the implementation stages of the application.

The document covers:
- The high-level system architecture
- The business logic layer design
- API interaction flows

The goal is to ensure clarity, consistency, and a shared understanding of the system design.

---

## High-Level Architecture

### Overview

The HBnB application follows a layered architecture that separates concerns between presentation, business logic, and persistence.  
A Facade pattern is used to simplify interactions between layers and ensure maintainability.

### High-Level Package Diagram

```mermaid
classDiagram
class PresentationLayer
class BusinessLogicLayer
class PersistenceLayer
class Facade

PresentationLayer --> Facade
Facade --> BusinessLogicLayer
BusinessLogicLayer --> PersistenceLayer
Explanation
Presentation Layer: Handles API requests and responses.

Facade: Acts as a single entry point to the business logic.

Business Logic Layer: Contains core application rules and entities.

Persistence Layer: Manages database interactions and data storage.

This structure improves scalability, testability, and separation of concerns.

Business Logic Layer
Overview
The Business Logic layer defines the core entities of the HBnB system and their relationships.
It encapsulates rules related to users, places, reviews, and amenities.

Class Diagram
mermaid
Copy code
classDiagram
class User {
    id : UUID
    first_name : string
    last_name : string
    email : string
    password : string
    is_admin : boolean
    created_at : datetime
    updated_at : datetime
}

class Place {
    id : UUID
    title : string
    description : string
    price : float
    latitude : float
    longitude : float
    created_at : datetime
    updated_at : datetime
}

class Review {
    id : UUID
    rating : int
    comment : string
    created_at : datetime
    updated_at : datetime
}

class Amenity {
    id : UUID
    name : string
    description : string
    created_at : datetime
    updated_at : datetime
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has
Explanation
User: Represents users of the system. A user can own places and write reviews.

Place: Represents a property listed in the system.

Review: Represents feedback provided by users for places.

Amenity: Represents features that can be associated with multiple places.

This design enforces clear ownership, relationships, and extensibility.

API Interaction Flow
Overview
Sequence diagrams illustrate how API requests flow through the system, from the presentation layer to the persistence layer.

Example: Create Place API
mermaid
Copy code
sequenceDiagram
participant Client
participant API
participant Facade
participant BusinessLogic
participant Database

Client ->> API: POST /places
API ->> Facade: create_place(data)
Facade ->> BusinessLogic: validate_and_create_place(data)
BusinessLogic ->> Database: save(place)
Database -->> BusinessLogic: success
BusinessLogic -->> Facade: place_created
Facade -->> API: response
API -->> Client: 201 Created
Explanation
The client sends a request to create a place.

The API forwards the request to the Facade.

Business logic validates and processes the data.

The place is stored in the database.

A success response is returned to the client.

This flow ensures validation, separation of concerns, and clean API handling.

Conclusion
This document consolidates the architectural vision and detailed design of the HBnB project.
It serves as a blueprint for development, ensuring consistency and clarity throughout the implementation process.

All diagrams and explanations align with best practices in software architecture and design.
