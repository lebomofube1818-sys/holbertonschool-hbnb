# Task 1: Detailed Class Diagram for Business Logic Layer

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
