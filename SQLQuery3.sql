DECLARE @TargetUserID INT = 4321;
DECLARE @TargetLevel INT;
DECLARE @TargetTrophy INT;
DECLARE @AvgTrophy FLOAT;
DECLARE @Result VARCHAR(20);

SELECT 
    @TargetLevel = Level,
    @TargetTrophy = Trophy
FROM 
    Users
WHERE 
    UserID = @TargetUserID;

SELECT 
    @AvgTrophy = AVG(CAST(Trophy AS FLOAT))
FROM 
    Users
WHERE 
    Level = @TargetLevel;

IF @TargetTrophy > @AvgTrophy + 300
    SET @Result = 'High';
ELSE IF @TargetTrophy < @AvgTrophy - 300
    SET @Result = 'Low';
ELSE
    SET @Result = 'Normal';

SELECT 
    @TargetUserID AS UserID,
    @TargetLevel AS Level,
    @TargetTrophy AS Trophy,
    @AvgTrophy AS AvgTrophyForLevel,
    @Result AS TrophyStatus;
