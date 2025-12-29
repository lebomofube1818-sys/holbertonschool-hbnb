classDiagram

class BaseEntity {
    +UUID id
    +DateTime created_at
    +DateTime updated_at
}

class User {
    +String first_name
    +String last_name
    +String email
    +String password
    +Boolean is_admin

    +create()
    +update()
    +delete()
}

class Place {
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude

    +create()
    +update()
    +delete()
}

class Review {
    +Integer rating
    +String comment

    +create()
    +update()
    +delete()
}

class Amenity {
    +String name
    +String description

    +create()
    +update()
    +delete()
}

BaseEntity <|-- User
BaseEntity <|-- Place
BaseEntity <|-- Review
BaseEntity <|-- Amenity

User "1" --> "0..*" Place : owns
User "1" --> "0..*" Review : writes
Place "1" --> "0..*" Review : has
Place "0..*" -- "0..*" Amenity : includes
