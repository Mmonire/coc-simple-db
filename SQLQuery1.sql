CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL,
    Level INT DEFAULT 1,
    Gold INT DEFAULT 0,
    Elixir INT DEFAULT 0,
    DarkElixir INT DEFAULT 0,
    Trophy INT DEFAULT 0,
    TownHallLevel INT NOT NULL,
    SignupDate DATETIME2(7) NOT NULL DEFAULT GETDATE()
);

CREATE TABLE Buildings (
    BuildingID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    UpgradeCost_Gold INT DEFAULT 0,
    UpgradeCost_Elixir INT DEFAULT 0,
    UpgradeCost_DarkElixir INT DEFAULT 0,
    Width INT NOT NULL,
    Height INT NOT NULL,
    Level INT DEFAULT 1,
    Type VARCHAR(20) NOT NULL CHECK (Type IN ('Defensive', 'Resource', 'Army'))
);

CREATE TABLE UserBuildings (
    UserBuildingID INT PRIMARY KEY IDENTITY(1,1),
    UserID INT NOT NULL,
    BuildingID INT NOT NULL,
    XCoordinate INT NOT NULL,
    YCoordinate INT NOT NULL,
    
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (BuildingID) REFERENCES Buildings(BuildingID)
);
CREATE TABLE Troops (
    TroopID INT PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    HitPoint INT NOT NULL,
    Damage INT NOT NULL,
    DamageType VARCHAR(20) NOT NULL CHECK (DamageType IN ('GroundToGround', 'GroundToAir', 'GroundToBoth', 'AirToBoth')),
    Capacity INT NOT NULL,
    Resource VARCHAR(20),
);

CREATE TABLE UserTroops (
    UserID INT NOT NULL,
    TroopID INT NOT NULL,
    Level INT NOT NULL,
    
    PRIMARY KEY (UserID, TroopID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (TroopID) REFERENCES Troops(TroopID),
);

CREATE TABLE Attacks (
    AttackID INT PRIMARY KEY IDENTITY(1,1),
    UserID_Offender INT NOT NULL,
    UserID_Defender INT NOT NULL,
    Castle_Destroyed DECIMAL(5,2) DEFAULT 0.00,
    Stars_achieved INT CHECK (Stars_achieved BETWEEN 0 AND 3),
    Attack_Time INT NOT NULL,
    
    FOREIGN KEY (UserID_Offender) REFERENCES Users(UserID),
    FOREIGN KEY (UserID_Defender) REFERENCES Users(UserID)
);
