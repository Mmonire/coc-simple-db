WITH SuccessfulDefenders AS (
    SELECT DISTINCT UserID_Defender AS UserID
    FROM Attacks
    WHERE Castle_Destroyed < 30.0 AND Stars_achieved <= 1
),
WallLevels AS (
    SELECT 
        ub.UserID,
        b.Level AS WallLevel
    FROM UserBuildings ub
    JOIN Buildings b ON ub.BuildingID = b.BuildingID
    WHERE b.Name LIKE '%Wall%'
),
WallAvg AS (
    SELECT AVG(CAST(WallLevel AS FLOAT)) AS AvgWallLevel
    FROM WallLevels
    WHERE UserID IN (SELECT UserID FROM SuccessfulDefenders)
),
TownHallAvg AS (
    SELECT AVG(CAST(TownHallLevel AS FLOAT)) AS AvgTownHallLevel
    FROM Users
    WHERE UserID IN (SELECT UserID FROM SuccessfulDefenders)
)
SELECT 
    w.AvgWallLevel,
    t.AvgTownHallLevel,
    ROUND(w.AvgWallLevel - t.AvgTownHallLevel, 2) AS LevelDifference
FROM WallAvg w, TownHallAvg t;