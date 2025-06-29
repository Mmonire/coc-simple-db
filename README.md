# Clash of Clans-Like Game Database Project

This project presents a fully structured and normalized relational database design for a simplified version of a Clash of Clans-like strategy game. The database supports essential gameplay features such as managing users, buildings, troops, and attacks.

---

## 📌 Features

- Track user profiles and their progress (resources, town hall level, trophies, etc.)
- Manage user-placed buildings with coordinates and levels
- Define and unlock troop types with upgrade levels
- Record and analyze attacks between users
- Track troops used and buildings destroyed in each attack
- Analyze user progression, troop efficiency, and strategic behavior
- Fully normalized up to **Third Normal Form (3NF)** (plus BCNF for `BuildingTypes`)

---

## 📐 Entity Descriptions

### 🧑‍💼 `Users`
- Primary Key: `UserID`
- Stores player details: username, level, resources, trophies, signup date, and town hall level.

### 🏗️ `Buildings`
- Primary Key: `BuildingID`
- References `BuildingTypes(Name)` to get building category (`Defensive`, `Resource`, `Army`)
- Stores upgrade costs, size, and level.

### 📋 `BuildingTypes`
- Primary Key: `Name`
- Specifies type/category of building (Defensive, Army, Resource)

### 🧱 `UserBuildings`
- Primary Key: `UserBuildingID`
- Links users with the buildings they’ve placed, including location (`XCoordinate`, `YCoordinate`).

### 🪖 `Troops`
- Primary Key: `TroopID`
- General troop definitions with attributes like hit points, damage, type, and resource type.

### 🔓 `UserTroops`
- Composite Key: `(UserID, TroopID)`
- Indicates which troops are unlocked for each user, and their current upgrade level.

### ⚔️ `Attacks`
- Primary Key: `AttackID`
- Captures battle details: attacker, defender, destruction percentage, stars earned, and attack duration.

### 🎯 `AttackTroops`
- Composite Key: `(AttackID, TroopID)`
- Shows how many of each troop type were used during a specific attack.

### 💥 `AttackDestroyedBuildings`
- Composite Key: `(AttackID, UserBuildingID)`
- Lists which buildings were destroyed in a specific attack.

---

## 🧠 Advanced Analysis Implemented

- **Recommended Troop Upgrade System**: Suggests troops for upgrade based on successful players of similar level.
- **Trophy Evaluation**: Classifies player trophies as High, Normal, or Low relative to average of their level group.
- **Player Efficiency Scoring**:
  - Measures how efficiently players convert time + resources into progress.
  - Detects behavior patterns:
    - Troop-Focused vs Building-Focused
    - Specialist vs Generalist
    - Dominant Building Type (e.g., Defensive-heavy base)
- **Defense Effectiveness**: Identifies users who successfully defend based on attack results.
- **Attack Timing Statistics**: For each level, calculates what % of attacks last under 60 seconds.
- **Most Effective Troops**: Tracks which troop types are most used in successful attacks by each player.

---

## ✅ Normalization Summary

| Table                      | Normalized To | Candidate Keys                      |
|---------------------------|---------------|-------------------------------------|
| Users                     | 3NF            | `UserID`                            |
| Buildings                 | BCNF           | `BuildingID`                        |
| BuildingTypes             | 3NF            | `Name`                              |
| UserBuildings             | 3NF            | `UserBuildingID`                    |
| Troops                    | 3NF            | `TroopID`                           |
| UserTroops                | 3NF            | `(UserID, TroopID)`                 |
| Attacks                   | 3NF            | `AttackID`                          |
| AttackTroops              | 3NF            | `(AttackID, TroopID)`               |
| AttackDestroyedBuildings  | 3NF            | `(AttackID, UserBuildingID)`        |
### 🛠️ Normalization Process: Step-by-Step

- In the original design, the Buildings table contained a Type field:
```
BuildingID | Name         | Type       | ...
-----------|--------------|------------|-----
1          | Archer Tower | Defensive  | ...
2          | Gold Mine    | Resource   | ...
```
- This caused a transitive functional dependency:
> BuildingID → Name → Type
- To fully normalize the schema (3NF and BCNF), we decomposed the table to remove this dependency.
- Step 1 – Create the new table `BuildingTypes`:
```sql
CREATE TABLE BuildingTypes (
    Name VARCHAR(50) PRIMARY KEY,
    Type VARCHAR(20) NOT NULL CHECK (Type IN ('Defensive', 'Resource', 'Army'))
);
```
- Step 2 – Populate `BuildingTypes` from existing `Buildings`:
```sql
INSERT INTO BuildingTypes (Name, Type)
SELECT DISTINCT Name, Type
FROM Buildings;
```
- Step 3 – Remove Type column from Buildings:
```sql
ALTER TABLE Buildings
DROP COLUMN Type;
```
- Step 4 – Add foreign key constraint from `Buildings` to `BuildingTypes`:
```sql
ALTER TABLE Buildings
ADD CONSTRAINT FK_Buildings_BuildingTypes
FOREIGN KEY (Name) REFERENCES BuildingTypes(Name);
```

---

## 🛠 Technologies Used

- SQL Server (Transact-SQL)
- ER Modeling (ERD link in project files)
- GitHub for version control
- Optional data generation: Python (for synthetic data)

---

## 🔗 ER Diagram
![1](https://github.com/user-attachments/assets/85729ec3-cda5-42b3-9fc0-12d0fe98d92e)
You can view the full ER diagram here:  
[📊 Canva ER Diagram](https://www.canva.com/design/DAGrWvRxBH4/YYErSmWDwxudfDbL_fd59Q/view)

---

## 🚀 Getting Started

To set up and test this database:

1. Run the provided SQL scripts in Microsoft SQL Server.
2. Populate sample data using data generators or manually.
3. Use the provided queries for analytics or integrate with a front-end UI.

---

## 📥 Future Enhancements

- Add timestamps for building/troop upgrades and attacks
- Introduce clan/guild systems
- Integrate with game simulation engine for real-time data

---

## 📧 Contact

Created by **Monire**  
For academic purposes
Contact via GitHub or telegram
