```mermaid
erDiagram
    USER {
        CHAR(36) id PK
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }

    PLACE {
        CHAR(36) id PK
        VARCHAR title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }

    REVIEW {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }

    AMENITY {
        CHAR(36) id PK
        VARCHAR name
    }

    PLACE_AMENITY {
        CHAR(36) place_id FK
        CHAR(36) amenity_id FK
    }

    %% Relationships
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ PLACE_AMENITY : has
    AMENITY ||--o{ PLACE_AMENITY : included_in


**Explanation:**

- `||--o{` → One-to-many (User → Place, User → Review, Place → Review)  
- `o{--o{` → Many-to-many (Place ↔ Amenity via Place_Amenity)  
- Attributes inside `{}` are table columns. `PK` for primary key, `FK` for foreign key.

---

### **Step 3 — Visualize in Mermaid Live Editor**

1. Go to [Mermaid Live Editor](https://mermaid.live/).  
2. Copy the Mermaid code from your file into the left editor panel.  
3. The ER diagram will render on the right.  
4. Make adjustments if something looks wrong (like relationships or column types).  

---

### **Step 4 — Export diagram for documentation**

- In Mermaid Live Editor, you can **export** as PNG or SVG.  
- Save it as `ER_Diagram.png` or `ER_Diagram.svg` in `part3/docs/` (create `docs/` if it doesn’t exist):

```bash
mkdir -p part3/docs
mv ~/Downloads/ER_Diagram.png part3/docs/
