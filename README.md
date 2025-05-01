# HR Analytics Dashboard

## Data Analysis

### Employee Performance Analysis

#### Employee Satisfaction Ratings

| Metric                     | Low (1-2) Impact               | High (4-5) Benefits           | Improvement Strategies         |
|----------------------------|--------------------------------|-------------------------------|--------------------------------|
| **Environmental**          | 42% higher stress              | 28% better focus              | Workspace upgrades             |
| **Job**                    | 3x attrition risk              | 32% productivity boost        | Career path programs           |
| **Relationship**           | 50% more conflicts             | 35% better collaboration      | Team-building activities       |
| **Work-Life Balance**      | 40% burnout rate               | 25% higher retention          | Flexible scheduling           |

#### Rating Discrepancies (Self vs Manager)

| Discrepancy Level | % Employees | Action Items                  |
|-------------------|-------------|-------------------------------|
| Self > +2         | 15%         | 360° feedback implementation  |
| Self > +1         | 22%         | Goal alignment workshops      |
| Within ±1         | 58%         | Recognition programs          |
| Self < -1         | 12%         | Performance coaching          |
| Self < -2         | 8%          | PIP development               |

### Attrition Analysis

#### Overall Metrics

| Metric                  | Value   | Industry Benchmark |
|-------------------------|---------|--------------------|
| Annual Attrition Rate   | 16.1%   | 12.4%              |
| Regrettable Attrition   | 62%     | 45-60%             |
| Avg Exit Tenure         | 2.8 yrs | 3.1 yrs            |
| Replacement Cost        | $1.3M   | -                  |

#### Department Breakdown

| Department   | Attrition Rate | Top Exit Reasons                          | Retention Actions                      |
|--------------|----------------|-------------------------------------------|----------------------------------------|
| Technology   | 20%            | Workload (45%), Travel (30%), Tools (25%) | Remote options, workload audits       |
| Sales        | 18%            | Stress (52%), Hours (38%), Targets (10%)  | Commission review, stress management  |
| HR           | 12%            | Growth (68%), Compensation (22%)          | Leadership pipeline, skill programs   |

#### Job Role Analysis

| Role                  | Attrition Rate | Avg Salary | Key Concerns               |
|-----------------------|----------------|------------|----------------------------|
| Software Engineers    | 22%            | $98,000    | Crunch time, tech debt     |
| Sales Representatives | 20%            | $85,000    | Unrealistic quotas        |
| Data Scientists       | 15%            | $112,000   | Limited production impact |
| HR Business Partners  | 10%            | $92,000    | Administrative workload   |

### Demographic Analysis

#### Age Distribution

| Age Group | % Workforce | Attrition Rate | Needs                      |
|-----------|-------------|----------------|----------------------------|
| <20       | 5%          | 8%             | Mentorship programs        |
| 20-29     | 30%         | 18%            | Career path clarity        |
| 30-39     | 40%         | 17%            | Work-life balance         |
| 40-49     | 20%         | 12%            | Health benefits           |
| 50+       | 5%          | 9%             | Phased retirement options |

#### Compensation Equity

| Ethnic Group           | % Workforce | Avg Salary | Pay Gap vs White |
|------------------------|-------------|------------|------------------|
| White                  | 60%         | $120,000   | 0%               |
| Black/African American | 20%         | $110,000   | -8.3%            |
| Asian                  | 15%         | $115,000   | -4.2%            |
| Other                  | 5%          | $105,000   | -12.5%           |

#### Gender Metrics

| Gender      | % Workforce | Attrition Rate | Avg Promotion Time |
|-------------|-------------|----------------|--------------------|
| Male        | 50%         | 14%            | 2.1 years          |
| Female      | 45%         | 18%            | 2.4 years          |
| Non-binary  | 3%          | 22%            | 2.7 years          |
| Undisclosed | 2%          | 15%            | 2.3 years          |

![Data](File/hr_dashboard.png)
![Data](File/hr_dashboard_2.png)

### Performance Trends

#### Quarterly Satisfaction Scores

| Quarter   | Job Sat | Env Sat | Rel Sat | Work-Life | Composite |
|-----------|---------|---------|---------|-----------|-----------|
| Q1 2022   | 4.2     | 3.9     | 4.5     | 4.0       | 4.15      |
| Q2 2022   | 4.0     | 3.7     | 4.6     | 3.8       | 4.03      |
| Q3 2022   | 3.8     | 3.5     | 4.7     | 3.6       | 3.90      |
| Q4 2022   | 3.6     | 3.3     | 4.8     | 3.4       | 3.78      |

#### Training Impact

| Sessions Completed | Performance Change | Retention Rate |
|--------------------|--------------------|----------------|
| 0                 | Baseline           | 78%            |
| 1-2               | +12%               | 84%            |
| 3-5               | +18%               | 89%            |
| 6+                | +25%               | 92%            |

## Technical Implementation

### Data Pipeline Steps

1. **Source Files**
   - Format: CSV/Excel
   - Tables: 12 raw tables
   - Size: 850MB total

2. **Cleaning Process**
   - Handled missing values (5.2% of cells)
   - Standardized rating scales (1-5)
   - Validated ID relationships

3. **Schema Transformation**
   - Created 1 fact table
   - Built 5 dimension tables
   - Established 12 relationships

### Key Scripts

| Script Name           | Purpose                          | Dependencies       |
|-----------------------|----------------------------------|--------------------|
| `data_validation.py`  | Verify data completeness         | Pandas 1.5.0       |
| `schema_builder.py`   | Create star schema               | SQLAlchemy 2.0     |
| `metrics_calculator.py` | Generate KPIs                   | NumPy 1.23.0       |

### Analysis Outputs

| Report Type          | Frequency   | Delivery Method     |
|----------------------|-------------|---------------------|
| Attrition Risk       | Weekly      | Email + Dashboard   |
| Satisfaction Trends  | Monthly     | PDF + PPT           |
| Diversity Metrics    | Quarterly   | Board Presentation  |

![Data](File/hr_dashboard_3.png)
![Data](File/hr_dashboard_4.png)
