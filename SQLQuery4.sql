WITH BuildingProgress AS (
    SELECT 
        ub.UserID,
        SUM(b.Level) AS TotalBuildingLevel,
        SUM(b.UpgradeCost_Gold + b.UpgradeCost_Elixir + b.UpgradeCost_DarkElixir) AS TotalBuildingCost
    FROM UserBuildings ub
    JOIN Buildings b ON ub.BuildingID = b.BuildingID
    GROUP BY ub.UserID
),
TroopProgress AS (
    SELECT 
        ut.UserID,
        SUM(ut.Level) AS TotalTroopLevel,
        COUNT(*) AS TotalTroopsUnlocked,
        COUNT(CASE WHEN Level >= 10 THEN 1 END) AS HighLevelTroops
    FROM UserTroops ut
    GROUP BY ut.UserID
),
DominantBuildingType AS (
    SELECT 
        UserID, Type, CountPerType
    FROM (
        SELECT 
            ub.UserID,
            b.Type,
            COUNT(*) AS CountPerType,
            ROW_NUMBER() OVER (PARTITION BY ub.UserID ORDER BY COUNT(*) DESC) AS rn
        FROM UserBuildings ub
        JOIN Buildings b ON ub.BuildingID = b.BuildingID
        GROUP BY ub.UserID, b.Type
    ) RankedTypes
    WHERE rn = 1
),
UserStats AS (
    SELECT 
        u.UserID,
        u.Username,
        u.SignupDate,
        u.TownHallLevel,
        ISNULL(bp.TotalBuildingLevel, 0) AS BuildingLevel,
        ISNULL(tp.TotalTroopLevel, 0) AS TroopLevel,
        ISNULL(bp.TotalBuildingCost, 0) AS TotalCost,
        ISNULL(tp.TotalTroopsUnlocked, 0) AS TotalTroopsUnlocked,
        ISNULL(tp.HighLevelTroops, 0) AS HighLevelTroops,
        ISNULL(bt.Type, 'Unknown') AS DominantBuildingType,
        DATEDIFF(SECOND, u.SignupDate, GETDATE()) AS ActiveSeconds
    FROM Users u
    LEFT JOIN BuildingProgress bp ON u.UserID = bp.UserID
    LEFT JOIN TroopProgress tp ON u.UserID = tp.UserID
    LEFT JOIN DominantBuildingType bt ON u.UserID = bt.UserID
),
Final AS (
    SELECT 
        *,
        (BuildingLevel + TroopLevel + TownHallLevel) AS TotalProgress,
        CAST((BuildingLevel + TroopLevel + TownHallLevel) AS FLOAT) / NULLIF(TotalCost + ActiveSeconds, 0) AS EfficiencyScore,
        CASE 
            WHEN TroopLevel > BuildingLevel THEN 'Troop Focused'
            ELSE 'Building Focused'
        END AS FocusType,
        CASE 
            WHEN CAST(HighLevelTroops AS FLOAT) / NULLIF(TotalTroopsUnlocked, 0) >= 0.7 THEN 'Specialist'
            ELSE 'Generalist'
        END AS TroopUpgradeStyle
    FROM UserStats
)
SELECT 
    UserID,
    Username,
    TownHallLevel,
    ROUND(EfficiencyScore, 6) AS EfficiencyScore,
    FocusType,
    DominantBuildingType,
    TroopUpgradeStyle,
    TotalProgress,
    TotalCost,
    ROUND(ActiveSeconds / 86400.0, 2) AS ActiveDays
FROM Final
ORDER BY EfficiencyScore DESC;
