# High-Level Package Diagram – HBnB Evolution

## Architecture Overview

```mermaid
classDiagram

package "Presentation Layer" {
    class API {
        <<Interface>>
        +handleRequests()
        +sendResponses()
    }
}

package "Business Logic Layer" {
    class HBnBFacade {
        <<Facade>>
        +createUser()
        +createPlace()
        +createReview()
        +listPlaces()
    }

    class User
    class Place
    class Review
    class Amenity
}

package "Persistence Layer" {
    class Repository {
        +save()
        +update()
        +delete()
        +find()
    }
}

API --> HBnBFacade : uses
HBnBFacade --> User : manages
HBnBFacade --> Place : manages
HBnBFacade --> Review : manages
HBnBFacade --> Amenity : manages
HBnBFacade --> Repository : persists data
