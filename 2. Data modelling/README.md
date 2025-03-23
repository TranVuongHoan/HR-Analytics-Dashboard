# Data Modelling

## Star Schema Structure

In this project, I used a **star schema structure** to organize the data for efficient querying and analysis. The star schema consists of a central fact table (`FactPerformanceRating`) surrounded by dimension tables (`DimEmployee`, `DimEducationLevel`, `DimDate`, `DimRatingLevel`, `DimSatisfiedLevel`). This structure allows for efficient data retrieval and analysis, particularly for HR analytics.

---

## Fact Table: `FactPerformanceRating`

- **`EmployeeID`**: The primary key (PK) for the fact table, uniquely identifying each employee.
- **`EnvironmentSatisfaction`**: Employee's satisfaction with the work environment (1-5 scale).
- **`JobSatisfaction`**: Employee's satisfaction with their job (1-5 scale).
- **`ManageRating`**: Manager's rating of the employee's performance (1-5 scale).
- **`PerformanceID`**: Unique identifier for each performance review.
- **`RelationshipSatisfaction`**: Employee's satisfaction with workplace relationships (1-5 scale).
- **`ReviewDate`**: Date of the performance review.
- **`SelfRating`**: Employee's self-rating of performance (1-5 scale).
- **`TrainingOpportunitiesTaken`**: Number of training opportunities taken.

---

## Dimension Tables

Each dimension table has a **many-to-one relationship** with the fact table, meaning multiple records in the fact table can relate to a single record in a dimension table.

### `DimEmployee`

- **`EmployeeID`**: The primary key (PK) that uniquely identifies each employee.
- **`Age`**: Employee's age.
- **`AgeBins`**: Age group categorization (e.g., *<20*, *20-29*, *30-39*, *40-49*, *50+*).
- **`Attrition`**: Whether the employee has left the company (*Yes/No*).
- **`BusinessTravel`**: Frequency of business travel (e.g., *Non-Travel*, *Travel_Rarely*, *Travel_Frequently*).
- **`Department`**: Employee's department (e.g., *Technology*, *Sales*, *Human Resources*).
- **`DistanceFromHome (KM)`**: Distance from home to workplace.
- **`Education`**: Education level (e.g., *High School*, *Bachelors*, *Masters*).
- **`EducationField`**: Field of education (e.g., *Life Sciences*, *Medical*, *Marketing*).
- **`Collapse`**: Additional details.

### `DimEducationLevel`

- **`EducationLevelID`**: The primary key (PK) that uniquely identifies each education level.
- **`EducationLevel`**: Description of the education level (e.g., *High School*, *Bachelors*, *Masters*).
- **`Collapse`**: Additional details.

### `DimDate`

- **`Date`**: The primary key (PK) that uniquely identifies each date.
- **`DayName`**: Name of the day (e.g., *Monday*, *Tuesday*).
- **`DayNameShort`**: Short name of the day (e.g., *Mon*, *Tue*).
- **`DayNumber`**: Day number in the month.
- **`DayOfWeek`**: Day of the week (e.g., *1* for Monday, *2* for Tuesday).
- **`Collapse`**: Additional details.

### `DimRatingLevel`

- **`RatingID`**: The primary key (PK) that uniquely identifies each rating level.
- **`RatingLevel`**: Description of the rating level (e.g., *Unacceptable*, *Meets Expectation*, *Exceeds Expectation*).
- **`Collapse`**: Additional details.

### `DimSatisfiedLevel`

- **`SatisfactionID`**: The primary key (PK) that uniquely identifies each satisfaction level.
- **`SatisfactionLevel`**: Description of the satisfaction level (e.g., *Very Dissatisfied*, *Neutral*, *Very Satisfied*).
- **`Collapse`**: Additional details.

---

This star schema structure ensures efficient data retrieval and analysis, enabling deeper insights into employee performance, satisfaction, and other HR metrics.
