DECLARE @TargetUserID INT = 3334;

WITH TargetUserLevel AS (
    SELECT Level FROM Users WHERE UserID = @TargetUserID
),
SuccessfulAttackers AS (
    SELECT DISTINCT a.UserID_Offender AS UserID
    FROM Attacks a
    JOIN Users u ON a.UserID_Offender = u.UserID
    JOIN TargetUserLevel tu ON ABS(u.Level - tu.Level) <= 2
    WHERE a.Stars_achieved >= 2 OR a.Castle_Destroyed >= 50.0
),
TroopUsageByPeers AS (
    SELECT ut.TroopID, COUNT(*) AS UsageCount
    FROM UserTroops ut
    JOIN SuccessfulAttackers sa ON ut.UserID = sa.UserID
    GROUP BY ut.TroopID
),
TargetUserTroops AS (
    SELECT TroopID, Level AS UserTroopLevel
    FROM UserTroops
    WHERE UserID = @TargetUserID
),
RecommendedTroops AS (
    SELECT 
        tb.TroopID,
        tr.Name,
        tu.UserTroopLevel,
        tb.UsageCount
    FROM TroopUsageByPeers tb
    JOIN Troops tr ON tb.TroopID = tr.TroopID
    LEFT JOIN TargetUserTroops tu ON tr.TroopID = tu.TroopID
    WHERE tu.TroopID IS NULL OR tu.UserTroopLevel < (
        SELECT AVG(Level) 
        FROM UserTroops ut
        WHERE ut.TroopID = tb.TroopID
    )
)
SELECT TOP 3 
    TroopID,
    Name AS RecommendedTroop,
    ISNULL(UserTroopLevel, 0) AS CurrentLevel,
    UsageCount AS PopularityAmongPeers
FROM RecommendedTroops
ORDER BY UsageCount DESC;
