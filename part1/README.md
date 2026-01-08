# Task 1: Detailed Class Diagram for Business Logic Layer

## Objective

This diagram represents the internal structure of the Business Logic layer of the HBnB application, showing the core entities, their attributes, methods, and relationships.

## Class Diagram

```mermaid
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

    create()
    update()
    delete()
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

    create()
    update()
    delete()
}

class Review {
    id : UUID
    rating : int
    comment : string
    created_at : datetime
    updated_at : datetime

    create()
    update()
    delete()
}

class Amenity {
    id : UUID
    name : string
    description : string
    created_at : datetime
    updated_at : datetime

    create()
    update()
    delete()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has

Explanatory Notes
User

Represents a user of the system. Users can be regular users or administrators. A user can own multiple places and write reviews.

Place

Represents a property listed in the system. Each place is owned by one user and can have multiple reviews and amenities.

Review

Represents feedback left by a user for a place. A review is associated with exactly one user and one place.

Amenity

Represents an amenity that can be associated with multiple places (e.g., Wi-Fi, Pool).

Relationships

A User can own multiple Places.

A User can write multiple Reviews.

A Place can receive multiple Reviews.

A Place can have multiple Amenities, and an Amenity can belong to multiple Places.
