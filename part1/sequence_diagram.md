# HBnB API Sequence Diagrams

---

##  User Registration

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /users (signup data)
API->>BusinessLogic: validate user data
BusinessLogic->>Database: create new User record
Database-->>BusinessLogic: return success
BusinessLogic-->>API: return user info
API-->>User: 201 Created / success message
```
Notes:

User data flows from API → BusinessLogic → Database

New user is created successfully

## Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /places (new place data)
API->>BusinessLogic: validate place data
BusinessLogic->>Database: save Place record
Database-->>BusinessLogic: confirmation saved
BusinessLogic-->>API: return place info
API-->>User: 201 Created / place details
```
Notes:

Adds a new rental listing

Validation and persistence handled by BusinessLogic and Database

## Review Submission

``mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: POST /reviews (review text, place_id)
API->>BusinessLogic: validate review & user_id
BusinessLogic->>Database: save Review record
Database-->>BusinessLogic: confirmation saved
BusinessLogic-->>API: return review info
API-->>User: 201 Created / review details
```
Notes:

User submits a review for a place

Review linked to both User & Place

## Fetching a List of Places

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: GET /places (optional filters)
API->>BusinessLogic: query places with filters
BusinessLogic->>Database: retrieve matching Place records
Database-->>BusinessLogic: return place list
BusinessLogic-->>API: return place list
API-->>User: 200 OK / list of places
```
Notes:

Shows data retrieval flow

Includes optional filtering logic in BusinessLogic

