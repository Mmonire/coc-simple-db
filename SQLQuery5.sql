WITH AttackData AS (
    SELECT 
        u.Level,
        a.Attack_Time,
        CASE WHEN a.Attack_Time < 60 THEN 1 ELSE 0 END AS IsUnderOneMinute
    FROM Attacks a
    JOIN Users u ON a.UserID_Offender = u.UserID
),
LevelStats AS (
    SELECT 
        Level,
        COUNT(*) AS TotalAttacks,
        SUM(IsUnderOneMinute) AS FastAttacks
    FROM AttackData
    GROUP BY Level
)
SELECT 
    Level,
    TotalAttacks,
    FastAttacks,
    ROUND(100.0 * FastAttacks / NULLIF(TotalAttacks, 0), 2) AS FastAttackPercentage
FROM LevelStats
ORDER BY Level;
