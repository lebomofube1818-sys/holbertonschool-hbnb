
classDiagram

class API
class Services

class Facade
class User
class Place
class Review
class Amenity

class Repository
class Database

API --> Facade : <<facade>>
Facade --> Repository : data access
