-- a. View all employees with their basic information
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Gender,
    Age,
    Department,
    JobRole,
    Salary,
    Education,
    EducationField
FROM Employee;

-- b. Count employees by department
SELECT 
    Department,
    COUNT(*) AS EmployeeCount
FROM Employee
GROUP BY Department
ORDER BY EmployeeCount DESC;

-- c. Average salary by department
SELECT 
    Department,
    AVG(Salary) AS AverageSalary,
    MIN(Salary) AS MinSalary,
    MAX(Salary) AS MaxSalary
FROM Employee
GROUP BY Department
ORDER BY AverageSalary DESC;

--  a. Employee distribution by education level
SELECT 
    el.EducationLevel,
    COUNT(*) AS EmployeeCount,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM Employee), 2) AS Percentage
FROM Employee e
JOIN EducationLevel el ON e.Education = el.EducationLevelID
GROUP BY el.EducationLevel
ORDER BY EmployeeCount DESC;

-- b. Average salary by education level
SELECT 
    el.EducationLevel,
    COUNT(*) AS EmployeeCount,
    AVG(e.Salary) AS AverageSalary,
    MIN(e.Salary) AS MinSalary,
    MAX(e.Salary) AS MaxSalary
FROM Employee e
JOIN EducationLevel el ON e.Education = el.EducationLevelID
GROUP BY el.EducationLevel
ORDER BY AverageSalary DESC;

-- c. Education level vs. job roles
SELECT 
    el.EducationLevel,
    e.JobRole,
    COUNT(*) AS EmployeeCount
FROM Employee e
JOIN EducationLevel el ON e.Education = el.EducationLevelID
GROUP BY el.EducationLevel, e.JobRole
ORDER BY el.EducationLevel, EmployeeCount DESC;

-- a. Performance ratings by employee
SELECT 
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    e.Department,
    pr.SelfRating,
    pr.ManagerRating,
    ROUND((pr.SelfRating + pr.ManagerRating) / 2.0, 2) AS AverageRating
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
ORDER BY AverageRating DESC;

-- b. Average ratings by department
SELECT 
    e.Department,
    COUNT(DISTINCT e.EmployeeID) AS EmployeeCount,
    AVG(pr.SelfRating) AS AvgSelfRating,
    AVG(pr.ManagerRating) AS AvgManagerRating,
    AVG((pr.SelfRating + pr.ManagerRating) / 2.0) AS AvgCombinedRating
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY e.Department
ORDER BY AvgCombinedRating DESC;

-- c. Rating distribution
SELECT 
    pr.SelfRating,
    COUNT(*) AS SelfRatingCount,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM PerformanceRating), 2) AS SelfRatingPercentage
FROM PerformanceRating pr
GROUP BY pr.SelfRating
ORDER BY pr.SelfRating;

-- a. Job satisfaction by department
SELECT 
    e.Department,
    COUNT(*) AS EmployeeCount,
    AVG(pr.JobSatisfaction) AS AvgJobSatisfaction,
    AVG(pr.EnvironmentSatisfaction) AS AvgEnvironmentSatisfaction,
    AVG(pr.RelationshipSatisfaction) AS AvgRelationshipSatisfaction
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY e.Department
ORDER BY AvgJobSatisfaction DESC;


-- b. Work-life balance analysis
SELECT 
    e.Department,
    pr.WorkLifeBalance,
    COUNT(*) AS EmployeeCount
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY e.Department, pr.WorkLifeBalance
ORDER BY e.Department, pr.WorkLifeBalance;

-- a. Rank employees by salary within each department
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    Salary,
    RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS SalaryRankInDept,
    RANK() OVER (ORDER BY Salary DESC) AS OverallSalaryRank
FROM Employee;


-- b. Top 3 highest paid employees per department
WITH RankedSalaries AS (
    SELECT 
        EmployeeID,
        FirstName,
        LastName,
        Department,
        Salary,
        RANK() OVER (PARTITION BY Department ORDER BY Salary DESC) AS SalaryRank
    FROM Employee
)
SELECT * FROM RankedSalaries 
WHERE SalaryRank <= 3
ORDER BY Department, SalaryRank;

-- c. Salary percentile within departments
SELECT 
    EmployeeID,
    FirstName,
    LastName,
    Department,
    Salary,
    NTILE(4) OVER (PARTITION BY Department ORDER BY Salary) AS SalaryQuartile
FROM Employee;

-- b. Department performance comparison
WITH DeptStats AS (
    SELECT 
        e.Department,
        COUNT(DISTINCT e.EmployeeID) AS EmployeeCount,
        AVG(e.Salary) AS AvgSalary,
        AVG(pr.SelfRating) AS AvgSelfRating,
        AVG(pr.ManagerRating) AS AvgManagerRating,
        AVG(pr.JobSatisfaction) AS AvgJobSatisfaction
    FROM Employee e
    JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
    GROUP BY e.Department
),
DeptRankings AS (
    SELECT 
        *,
        RANK() OVER (ORDER BY AvgSalary DESC) AS SalaryRank,
        RANK() OVER (ORDER BY AvgSelfRating DESC) AS SelfRatingRank,
        RANK() OVER (ORDER BY AvgManagerRating DESC) AS ManagerRatingRank,
        RANK() OVER (ORDER BY AvgJobSatisfaction DESC) AS SatisfactionRank
    FROM DeptStats
)
SELECT * FROM DeptRankings;

-- a. Employees earning above average salary in their department
SELECT 
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    e.Department,
    e.Salary,
    (SELECT AVG(Salary) FROM Employee WHERE Department = e.Department) AS DeptAvgSalary
FROM Employee e
WHERE e.Salary > (SELECT AVG(Salary) FROM Employee WHERE Department = e.Department)
ORDER BY e.Department, e.Salary DESC;

-- b. Employees with highest satisfaction in their department
SELECT 
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    e.Department,
    pr.JobSatisfaction
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
WHERE pr.JobSatisfaction = (
    SELECT MAX(pr2.JobSatisfaction) 
    FROM PerformanceRating pr2 
    JOIN Employee e2 ON pr2.EmployeeID = e2.EmployeeID 
    WHERE e2.Department = e.Department
)
ORDER BY e.Department, pr.JobSatisfaction DESC;


-- b. Training opportunities analysis
SELECT 
    e.Department,
    COUNT(*) AS TotalEmployees,
    AVG(pr.TrainingOpportunitiesWithinYear) AS AvgTrainingOffered,
    AVG(pr.TrainingOpportunitiesTaken) AS AvgTrainingTaken,
    ROUND(100.0 * AVG(pr.TrainingOpportunitiesTaken) / NULLIF(AVG(pr.TrainingOpportunitiesWithinYear), 0), 2) AS TrainingUtilizationRate
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY e.Department
ORDER BY TrainingUtilizationRate DESC;

-- c. Gender diversity analysis
SELECT 
    e.Department,
    e.Gender,
    COUNT(*) AS EmployeeCount,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY e.Department), 2) AS GenderPercentage
FROM Employee e
GROUP BY e.Department, e.Gender
ORDER BY e.Department, EmployeeCount DESC;

-- a. Employee satisfaction vs. performance correlation
WITH SatisfactionPerformance AS (
    SELECT 
        e.EmployeeID,
        e.Department,
        pr.JobSatisfaction,
        pr.EnvironmentSatisfaction,
        pr.RelationshipSatisfaction,
        (pr.SelfRating + pr.ManagerRating) / 2.0 AS AvgPerformanceRating
    FROM Employee e
    JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
),
CorrelationData AS (
    SELECT 
        Department,
        COUNT(*) AS EmployeeCount,
        AVG(JobSatisfaction) AS AvgJobSatisfaction,
        AVG(AvgPerformanceRating) AS AvgPerformance,
        AVG(JobSatisfaction * AvgPerformanceRating) AS AvgProduct,
        AVG(JobSatisfaction * JobSatisfaction) AS AvgJobSatisfactionSquared,
        AVG(AvgPerformanceRating * AvgPerformanceRating) AS AvgPerformanceSquared
    FROM SatisfactionPerformance
    GROUP BY Department
)
SELECT 
    Department,
    EmployeeCount,
    AvgJobSatisfaction,
    AvgPerformance,
    CASE 
        WHEN (AvgJobSatisfactionSquared - AvgJobSatisfaction * AvgJobSatisfaction) * 
             (AvgPerformanceSquared - AvgPerformance * AvgPerformance) = 0 
        THEN NULL
        ELSE 
            (AvgProduct - AvgJobSatisfaction * AvgPerformance) / 
            SQRT((AvgJobSatisfactionSquared - AvgJobSatisfaction * AvgJobSatisfaction) * 
                 (AvgPerformanceSquared - AvgPerformance * AvgPerformance))
    END AS SatisfactionPerformanceCorrelation
FROM CorrelationData
ORDER BY SatisfactionPerformanceCorrelation DESC;

-- b. Age group analysis
SELECT 
    CASE 
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age BETWEEN 30 AND 40 THEN '30-40'
        WHEN Age BETWEEN 41 AND 50 THEN '41-50'
        ELSE 'Over 50'
    END AS AgeGroup,
    COUNT(*) AS EmployeeCount,
    AVG(Salary) AS AvgSalary,
    AVG(pr.JobSatisfaction) AS AvgJobSatisfaction,
    AVG(pr.SelfRating) AS AvgSelfRating
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY 
    CASE 
        WHEN Age < 30 THEN 'Under 30'
        WHEN Age BETWEEN 30 AND 40 THEN '30-40'
        WHEN Age BETWEEN 41 AND 50 THEN '41-50'
        ELSE 'Over 50'
    END
ORDER BY AgeGroup;

-- a. Missing performance data
SELECT 
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    e.Department
FROM Employee e
LEFT JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
WHERE pr.EmployeeID IS NULL;

-- b. Data consistency check
SELECT 
    'Employees with Education Level not in EducationLevel table' AS Issue,
    COUNT(*) AS Count
FROM Employee e
LEFT JOIN EducationLevel el ON e.Education = el.EducationLevelID
WHERE el.EducationLevelID IS NULL

UNION ALL

SELECT 
    'Performance records without matching employees' AS Issue,
    COUNT(*) AS Count
FROM PerformanceRating pr
LEFT JOIN Employee e ON pr.EmployeeID = e.EmployeeID
WHERE e.EmployeeID IS NULL;

-- a. High-potential employee identification
WITH EmployeeScores AS (
    SELECT 
        e.EmployeeID,
        e.FirstName,
        e.LastName,
        e.Department,
        e.Salary,
        pr.SelfRating,
        pr.ManagerRating,
        pr.JobSatisfaction,
        pr.EnvironmentSatisfaction,
        pr.RelationshipSatisfaction,
        pr.WorkLifeBalance,
        (pr.SelfRating + pr.ManagerRating) / 2.0 AS AvgPerformance,
        (pr.JobSatisfaction + pr.EnvironmentSatisfaction + pr.RelationshipSatisfaction + pr.WorkLifeBalance) / 4.0 AS AvgSatisfaction
    FROM Employee e
    JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
)
SELECT 
    *,
    CASE 
        WHEN AvgPerformance >= 4 AND AvgSatisfaction >= 4 THEN 'High Potential'
        WHEN AvgPerformance >= 4 AND AvgSatisfaction < 4 THEN 'High Performer - Needs Engagement'
        WHEN AvgPerformance < 4 AND AvgSatisfaction >= 4 THEN 'Engaged - Needs Development'
        ELSE 'Needs Attention'
    END AS EmployeeCategory
FROM EmployeeScores
ORDER BY AvgPerformance DESC, AvgSatisfaction DESC;

-- b. Department health score
SELECT 
    e.Department,
    COUNT(DISTINCT e.EmployeeID) AS EmployeeCount,
    AVG(e.Salary) AS AvgSalary,
    AVG(pr.JobSatisfaction) AS AvgJobSatisfaction,
    AVG((pr.SelfRating + pr.ManagerRating) / 2.0) AS AvgPerformance,
    SUM(CASE WHEN CAST(e.Attrition AS VARCHAR(10)) = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS AttritionRate,
    ROUND(
        (AVG(pr.JobSatisfaction) * 0.3 + 
         AVG((pr.SelfRating + pr.ManagerRating) / 2.0) * 0.4 + 
         (100 - SUM(CASE WHEN CAST(e.Attrition AS VARCHAR(10)) = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) * 0.3), 2
    ) AS HealthScore
FROM Employee e
JOIN PerformanceRating pr ON e.EmployeeID = pr.EmployeeID
GROUP BY e.Department
ORDER BY HealthScore DESC;