# HBnB Technical Documentation

---

## Introduction

The purpose of this document is to provide a comprehensive technical blueprint for the HBnB project.  
It consolidates all architecture and design diagrams, along with explanatory notes, to guide the implementation phase and serve as a reference for developers.

This document covers:

- High-Level Architecture (Package Diagram)  
- Business Logic Layer (Class Diagram)  
- API Interaction Flow (Sequence Diagrams)  

---

## High-Level Architecture

### Layered Architecture Overview

The HBnB application uses a three-layer architecture:

1. **Presentation Layer**: Handles user interactions via API and services.  
2. **Business Logic Layer**: Contains the core models representing entities like User, Place, Review, and Amenity.  
3. **Persistence Layer**: Responsible for data storage and retrieval from the database.  

The **Facade Pattern** is used to simplify communication between layers by providing a unified interface.

### High-Level Package Diagram

```mermaid
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
```
Notes:

Shows the three-layer architecture

API and Services interact with Business Logic through the Facade

Repository communicates with Database for persistence
