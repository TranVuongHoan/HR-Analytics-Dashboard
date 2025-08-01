import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

class HRAnalyticsPreprocessor:
    def __init__(self):
        self.employee_df = None
        self.education_df = None
        self.performance_df = None
        self.rating_df = None
        self.satisfaction_df = None
        self.merged_df = None
        
    def load_data(self):
        """Load all CSV files"""
        print("Loading CSV files...")
        
        try:
            self.employee_df = pd.read_csv('Employee.csv')
            self.education_df = pd.read_csv('EducationLevel.csv')
            self.performance_df = pd.read_csv('PerformanceRating.csv')
            self.rating_df = pd.read_csv('RatingLevel.csv')
            self.satisfaction_df = pd.read_csv('SatisfiedLevel.csv')
            
            print("✅ All files loaded successfully!")
            print(f"Employee records: {len(self.employee_df)}")
            print(f"Performance records: {len(self.performance_df)}")
            
        except Exception as e:
            print(f"❌ Error loading files: {e}")
            return False
        
        return True
    
    def clean_employee_data(self):
        """Clean and preprocess employee data"""
        print("\n🧹 Cleaning employee data...")
        
        # Remove duplicates
        initial_count = len(self.employee_df)
        self.employee_df = self.employee_df.drop_duplicates()
        print(f"Removed {initial_count - len(self.employee_df)} duplicate records")
        
        # Handle missing values
        missing_before = self.employee_df.isnull().sum().sum()
        
        # Fill missing values with appropriate defaults
        self.employee_df['Gender'].fillna('Unknown', inplace=True)
        self.employee_df['Age'].fillna(self.employee_df['Age'].median(), inplace=True)
        self.employee_df['Salary'].fillna(self.employee_df['Salary'].median(), inplace=True)
        
        missing_after = self.employee_df.isnull().sum().sum()
        print(f"Handled {missing_before - missing_after} missing values")
        
        # Convert data types
        self.employee_df['Age'] = pd.to_numeric(self.employee_df['Age'], errors='coerce')
        self.employee_df['Salary'] = pd.to_numeric(self.employee_df['Salary'], errors='coerce')
        self.employee_df['YearsAtCompany'] = pd.to_numeric(self.employee_df['YearsAtCompany'], errors='coerce')
        
        # Convert HireDate to datetime
        self.employee_df['HireDate'] = pd.to_datetime(self.employee_df['HireDate'], errors='coerce')
        
        print("✅ Employee data cleaned!")
    
    def clean_performance_data(self):
        """Clean and preprocess performance data"""
        print("\n🧹 Cleaning performance data...")
        
        # Remove duplicates
        initial_count = len(self.performance_df)
        self.performance_df = self.performance_df.drop_duplicates()
        print(f"Removed {initial_count - len(self.performance_df)} duplicate records")
        
        # Convert ReviewDate to datetime
        self.performance_df['ReviewDate'] = pd.to_datetime(self.performance_df['ReviewDate'], errors='coerce')
        
        # Handle missing values
        numeric_columns = ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction', 
                          'TrainingOpportunitiesWithinYear', 'TrainingOpportunitiesTaken', 
                          'WorkLifeBalance', 'SelfRating', 'ManagerRating']
        
        for col in numeric_columns:
            if col in self.performance_df.columns:
                self.performance_df[col].fillna(self.performance_df[col].median(), inplace=True)
        
        print("✅ Performance data cleaned!")
    
    def merge_data(self):
        """Merge all datasets"""
        print("\n🔗 Merging datasets...")
        
        # Merge employee with education
        self.merged_df = self.employee_df.merge(
            self.education_df, 
            left_on='Education', 
            right_on='EducationLevelID', 
            how='left'
        )
        
        # Merge with performance data
        self.merged_df = self.merged_df.merge(
            self.performance_df, 
            on='EmployeeID', 
            how='left'
        )
        
        print(f"✅ Merged dataset created with {len(self.merged_df)} records")
    
    def create_features(self):
        """Create new features for analysis"""
        print("\n🔧 Creating new features...")
        
        # Age groups
        self.merged_df['AgeGroup'] = pd.cut(
            self.merged_df['Age'], 
            bins=[0, 30, 40, 50, 100], 
            labels=['Under 30', '30-40', '40-50', 'Over 50']
        )
        
        # Salary ranges
        self.merged_df['SalaryRange'] = pd.cut(
            self.merged_df['Salary'], 
            bins=5, 
            labels=['Low', 'Below Average', 'Average', 'Above Average', 'High']
        )
        
        # Performance score (average of self and manager rating)
        self.merged_df['PerformanceScore'] = (
            self.merged_df['SelfRating'] + self.merged_df['ManagerRating']
        ) / 2
        
        # Overall satisfaction score
        satisfaction_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'RelationshipSatisfaction']
        self.merged_df['OverallSatisfaction'] = self.merged_df[satisfaction_cols].mean(axis=1)
        
        # Training utilization rate
        self.merged_df['TrainingUtilization'] = np.where(
            self.merged_df['TrainingOpportunitiesWithinYear'] > 0,
            self.merged_df['TrainingOpportunitiesTaken'] / self.merged_df['TrainingOpportunitiesWithinYear'],
            0
        )
        
        # Tenure categories
        self.merged_df['TenureCategory'] = pd.cut(
            self.merged_df['YearsAtCompany'], 
            bins=[0, 2, 5, 10, 100], 
            labels=['New', 'Early Career', 'Mid Career', 'Long Term']
        )
        
        # Performance categories
        self.merged_df['PerformanceCategory'] = pd.cut(
            self.merged_df['PerformanceScore'], 
            bins=[0, 2, 3, 4, 5], 
            labels=['Needs Improvement', 'Meets Expectations', 'Exceeds Expectations', 'Outstanding']
        )
        
        # Risk score for attrition
        self.merged_df['AttritionRisk'] = (
            (5 - self.merged_df['JobSatisfaction']) * 0.3 +
            (5 - self.merged_df['WorkLifeBalance']) * 0.2 +
            (5 - self.merged_df['OverallSatisfaction']) * 0.3 +
            (self.merged_df['YearsAtCompany'] < 2) * 0.2
        )
        
        print("✅ New features created!")
    
    def create_aggregated_tables(self):
        """Create aggregated tables for Power BI"""
        print("\n📊 Creating aggregated tables...")
        
        # Department summary
        dept_summary = self.merged_df.groupby('Department').agg({
            'EmployeeID': 'count',
            'Salary': ['mean', 'min', 'max'],
            'Age': 'mean',
            'JobSatisfaction': 'mean',
            'PerformanceScore': 'mean',
            'Attrition': lambda x: (x == 'Yes').sum(),
            'WorkLifeBalance': 'mean'
        }).round(2)
        
        dept_summary.columns = ['EmployeeCount', 'AvgSalary', 'MinSalary', 'MaxSalary', 
                               'AvgAge', 'AvgJobSatisfaction', 'AvgPerformance', 
                               'AttritionCount', 'AvgWorkLifeBalance']
        dept_summary['AttritionRate'] = (dept_summary['AttritionCount'] / dept_summary['EmployeeCount'] * 100).round(2)
        
        # Education level analysis
        education_summary = self.merged_df.groupby('EducationLevel').agg({
            'EmployeeID': 'count',
            'Salary': 'mean',
            'PerformanceScore': 'mean',
            'JobSatisfaction': 'mean',
            'Attrition': lambda x: (x == 'Yes').sum()
        }).round(2)
        
        education_summary.columns = ['EmployeeCount', 'AvgSalary', 'AvgPerformance', 
                                   'AvgJobSatisfaction', 'AttritionCount']
        education_summary['AttritionRate'] = (education_summary['AttritionCount'] / education_summary['EmployeeCount'] * 100).round(2)
        
        # Age group analysis
        age_summary = self.merged_df.groupby('AgeGroup').agg({
            'EmployeeID': 'count',
            'Salary': 'mean',
            'PerformanceScore': 'mean',
            'JobSatisfaction': 'mean',
            'Attrition': lambda x: (x == 'Yes').sum()
        }).round(2)
        
        age_summary.columns = ['EmployeeCount', 'AvgSalary', 'AvgPerformance', 
                              'AvgJobSatisfaction', 'AttritionCount']
        age_summary['AttritionRate'] = (age_summary['AttritionCount'] / age_summary['EmployeeCount'] * 100).round(2)
        
        # Performance trends over time
        performance_trends = self.merged_df.groupby(['Department', 'ReviewDate']).agg({
            'PerformanceScore': 'mean',
            'JobSatisfaction': 'mean',
            'EmployeeID': 'count'
        }).reset_index()
        
        # Save aggregated tables
        dept_summary.to_csv('department_summary.csv', index=True)
        education_summary.to_csv('education_summary.csv', index=True)
        age_summary.to_csv('age_summary.csv', index=True)
        performance_trends.to_csv('performance_trends.csv', index=False)
        
        print("✅ Aggregated tables created and saved!")
        
        return dept_summary, education_summary, age_summary, performance_trends
    
    def generate_insights(self):
        """Generate key insights and statistics"""
        print("\n📈 Generating insights...")
        
        insights = {}
        
        # Overall statistics
        insights['total_employees'] = len(self.employee_df)
        insights['attrition_rate'] = (self.employee_df['Attrition'] == 'Yes').mean() * 100
        insights['avg_salary'] = self.employee_df['Salary'].mean()
        insights['avg_age'] = self.employee_df['Age'].mean()
        
        # Department insights
        dept_attrition = self.employee_df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).sort_values(ascending=False)
        
        insights['highest_attrition_dept'] = dept_attrition.index[0]
        insights['highest_attrition_rate'] = dept_attrition.iloc[0]
        
        # Performance insights
        if 'PerformanceScore' in self.merged_df.columns:
            insights['avg_performance'] = self.merged_df['PerformanceScore'].mean()
            insights['top_performers'] = (self.merged_df['PerformanceScore'] >= 4).sum()
        
        # Satisfaction insights
        if 'OverallSatisfaction' in self.merged_df.columns:
            insights['avg_satisfaction'] = self.merged_df['OverallSatisfaction'].mean()
            insights['highly_satisfied'] = (self.merged_df['OverallSatisfaction'] >= 4).sum()
        
        print("Key Insights:")
        for key, value in insights.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        return insights
    
    def create_visualizations(self):
        """Create basic visualizations"""
        print("\n📊 Creating visualizations...")
        
        # Set style
        try:
            plt.style.use('seaborn-v0_8')
        except:
            plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Attrition by Department
        attrition_by_dept = self.employee_df.groupby('Department')['Attrition'].apply(
            lambda x: (x == 'Yes').sum()
        )
        attrition_by_dept.plot(kind='bar', ax=axes[0,0], title='Attrition by Department')
        axes[0,0].set_ylabel('Number of Attritions')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # 2. Salary Distribution
        self.employee_df['Salary'].hist(bins=30, ax=axes[0,1])
        axes[0,1].set_title('Salary Distribution')
        axes[0,1].set_xlabel('Salary')
        axes[0,1].set_ylabel('Frequency')
        
        # 3. Age Distribution
        self.employee_df['Age'].hist(bins=20, ax=axes[1,0])
        axes[1,0].set_title('Age Distribution')
        axes[1,0].set_xlabel('Age')
        axes[1,0].set_ylabel('Frequency')
        
        # 4. Education Level Distribution
        if 'EducationLevel' in self.merged_df.columns:
            self.merged_df['EducationLevel'].value_counts().plot(
                kind='pie', ax=axes[1,1], title='Education Level Distribution'
            )
        
        plt.tight_layout()
        plt.savefig('hr_analytics_overview.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizations saved as 'hr_analytics_overview.png'")
    
    def export_for_powerbi(self):
        """Export processed data for Power BI"""
        print("\n💾 Exporting data for Power BI...")
        
        # Export main merged dataset
        self.merged_df.to_csv('hr_analytics_processed.csv', index=False)
        
        # Export individual cleaned datasets
        self.employee_df.to_csv('employee_cleaned.csv', index=False)
        self.performance_df.to_csv('performance_cleaned.csv', index=False)
        
        # Create a summary report
        with open('data_processing_report.txt', 'w') as f:
            f.write("HR Analytics Data Processing Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Total Employees: {len(self.employee_df)}\n")
            f.write(f"Total Performance Records: {len(self.performance_df)}\n")
            f.write(f"Data Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Files Created:\n")
            f.write("- hr_analytics_processed.csv (Main dataset for Power BI)\n")
            f.write("- employee_cleaned.csv (Cleaned employee data)\n")
            f.write("- performance_cleaned.csv (Cleaned performance data)\n")
            f.write("- department_summary.csv (Department aggregations)\n")
            f.write("- education_summary.csv (Education level analysis)\n")
            f.write("- age_summary.csv (Age group analysis)\n")
            f.write("- performance_trends.csv (Performance trends)\n")
        
        print("✅ Data exported for Power BI!")
        print("📁 Files created:")
        print("  - hr_analytics_processed.csv (Main dataset)")
        print("  - employee_cleaned.csv")
        print("  - performance_cleaned.csv")
        print("  - Various summary tables")
        print("  - data_processing_report.txt")
    
    def run_full_pipeline(self):
        """Run the complete data processing pipeline"""
        print("🚀 Starting HR Analytics Data Processing Pipeline")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            return False
        
        # Clean data
        self.clean_employee_data()
        self.clean_performance_data()
        
        # Merge data
        self.merge_data()
        
        # Create features
        self.create_features()
        
        # Create aggregated tables
        self.create_aggregated_tables()
        
        # Generate insights
        self.generate_insights()
        
        # Create visualizations
        self.create_visualizations()
        
        # Export for Power BI
        self.export_for_powerbi()
        
        print("\n🎉 Pipeline completed successfully!")
        return True

# Main execution
if __name__ == "__main__":
    # Initialize preprocessor
    preprocessor = HRAnalyticsPreprocessor()
    
    # Run the full pipeline
    success = preprocessor.run_full_pipeline()
    
    if success:
        print("\n📊 Your data is ready for Power BI!")
        print("Import 'hr_analytics_processed.csv' as your main dataset in Power BI.")
    else:
        print("\n❌ Pipeline failed. Please check your CSV files.") 