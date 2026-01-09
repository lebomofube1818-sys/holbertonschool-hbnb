# HBnB Architecture Documentation

## High-Level Package Diagram

```mermaid
classDiagram

%% Classes with attributes and methods
class User {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +string email
    +string password
    +string first_name
    +string last_name
    +save()
    +to_dict()
}

class Place {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +string name
    +string description
    +int number_rooms
    +int number_bathrooms
    +int max_guest
    +int price_by_night
    +save()
    +to_dict()
}

class Review {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +string text
    +string user_id
    +string place_id
    +save()
    +to_dict()
}

class Amenity {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +string name
    +save()
    +to_dict()
}

%% Relationships
User "1" --> "*" Review : writes
Place "1" --> "*" Review : has
Place "*" --> "*" Amenity : includes
Amenity "*" --> "*" Place : belongs_to
```
Business Logic Layer Overview

User
Represents a registered user. Stores login credentials and personal information. Responsible for writing Reviews.

Place
Represents a rental property. Stores attributes like rooms, bathrooms, max guests, and price. Can have multiple Reviews and multiple Amenities.

Review
Represents a review left by a User for a Place. Linked to both User and Place. Contains textual feedback.

Amenity
Represents a feature of a Place (e.g., Wi-Fi, pool). Many-to-many relationship with Place.

Relationships

User → Review: one-to-many

Place → Review: one-to-many

Place ↔ Amenity: many-to-many
