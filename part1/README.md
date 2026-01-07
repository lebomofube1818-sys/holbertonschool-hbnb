# HBnB # Task 1: Detailed Class Diagram for Business Logic Layer
## Objective

This diagram represents the internal structure of the Business Logic layer of the HBnB application, showing the core entities, their attributes, methods, and relationships.
## Class Diagram

```mermaid
classDiagram
class User {
    +UUID id
    +string first_name
    +string last_name
    +string email
    +string password
    +boolean is_admin
    +datetime created_at
    +datetime updated_at

    +create()
    +update()
    +delete()
}

class Place {
    +UUID id
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +datetime created_at
    +datetime updated_at

    +create()
    +update()
    +delete()
}

class Review {
    +UUID id
    +int rating
    +string comment
    +datetime created_at
    +datetime updated_at

    +create()
    +update()
    +delete()
}

class Amenity {
    +UUID id
    +string name
    +string description
    +datetime created_at
    +datetime updated_at

    +create()
    +update()
    +delete()
}

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : receives
Place "0..*" --> "0..*" Amenity : has

```markdown
## Explanatory Notes

### User
Represents a user of the system. Users can be regular users or administrators. A user can own multiple places and write reviews.

### Place
Represents a property listed in the system. Each place is owned by one user and can have multiple reviews and amenities.

### Review
Represents feedback left by a user for a place. A review is associated with exactly one user and one place.

### Amenity
Represents an amenity that can be associated with multiple places (e.g., Wi-Fi, Pool).

### Relationships
- A User can own multiple Places.
- A User can write multiple Reviews.
- A Place can receive multiple Reviews.
- A Place can have multiple Amenities, and an Amenity can belong to multiple Places.
