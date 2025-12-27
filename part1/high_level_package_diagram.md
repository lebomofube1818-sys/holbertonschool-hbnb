classDiagram

class API {
    <<Presentation>>
    +handleRequests()
    +sendResponses()
}

class HBnBFacade {
    <<Facade>>
    +createUser()
    +createPlace()
    +createReview()
    +listPlaces()
}

class User {
    <<BusinessLogic>>
}

class Place {
    <<BusinessLogic>>
}

class Review {
    <<BusinessLogic>>
}

class Amenity {
    <<BusinessLogic>>
}

class Repository {
    <<Persistence>>
    +save()
    +update()
    +delete()
    +find()
}

API --> HBnBFacade : uses
HBnBFacade --> User : manages
HBnBFacade --> Place : manages
HBnBFacade --> Review : manages
HBnBFacade --> Amenity : manages
HBnBFacade --> Repository : persists data
