import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif
import warnings
warnings.filterwarnings('ignore')

class HRAdvancedAnalytics:
    def __init__(self):
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self):
        """Load the processed HR data"""
        print("📊 Loading processed HR data...")
        try:
            self.data = pd.read_csv('hr_analytics_processed.csv')
            print(f"✅ Data loaded successfully! Shape: {self.data.shape}")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            print("Make sure to run hr_analytics_preprocessing.py first to create the processed data file.")
            return False
    
    def prepare_attrition_data(self):
        """Prepare data for attrition prediction"""
        print("\n🔧 Preparing data for attrition prediction...")
        
        # Select features for attrition prediction
        feature_columns = [
            'Age', 'Salary', 'YearsAtCompany', 'YearsInMostRecentRole',
            'YearsSinceLastPromotion', 'YearsWithCurrManager', 'JobSatisfaction',
            'EnvironmentSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance',
            'SelfRating', 'ManagerRating', 'PerformanceScore', 'OverallSatisfaction',
            'TrainingUtilization', 'AttritionRisk'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_columns if col in self.data.columns]
        
        # Prepare features
        self.X = self.data[available_features].copy()
        
        # Handle missing values
        self.X = self.X.fillna(self.X.median())
        
        # Prepare target variable
        self.y = (self.data['Attrition'] == 'Yes').astype(int)
        
        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42, stratify=self.y
        )
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        print(f"✅ Data prepared! Features: {len(available_features)}, Train: {len(self.X_train)}, Test: {len(self.X_test)}")
        print(f"Attrition rate: {self.y.mean():.2%}")
    
    def train_attrition_models(self):
        """Train multiple models for attrition prediction"""
        print("\n🤖 Training attrition prediction models...")
        
        # Define models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Gradient Boosting': GradientBoostingClassifier(random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000)
        }
        
        # Train and evaluate models
        results = {}
        
        for name, model in models.items():
            print(f"Training {name}...")
            
            # Train model
            if name == 'Logistic Regression':
                model.fit(self.X_train_scaled, self.y_train)
                y_pred = model.predict(self.X_test_scaled)
                y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
            else:
                model.fit(self.X_train, self.y_train)
                y_pred = model.predict(self.X_test)
                y_pred_proba = model.predict_proba(self.X_test)[:, 1]
            
            # Calculate metrics
            auc_score = roc_auc_score(self.y_test, y_pred_proba)
            accuracy = (y_pred == self.y_test).mean()
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'auc_score': auc_score,
                'y_pred': y_pred,
                'y_pred_proba': y_pred_proba
            }
            
            print(f"  {name} - Accuracy: {accuracy:.3f}, AUC: {auc_score:.3f}")
        
        self.models = results
        return results
    
    def feature_importance_analysis(self):
        """Analyze feature importance for attrition prediction"""
        print("\n📈 Analyzing feature importance...")
        
        # Get feature importance from Random Forest
        rf_model = self.models['Random Forest']['model']
        feature_importance = pd.DataFrame({
            'feature': self.X.columns,
            'importance': rf_model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Plot feature importance
        plt.figure(figsize=(12, 8))
        sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
        plt.title('Top 10 Most Important Features for Attrition Prediction')
        plt.xlabel('Feature Importance')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Feature importance analysis completed!")
        return feature_importance
    
    def employee_clustering(self):
        """Perform employee clustering analysis"""
        print("\n🎯 Performing employee clustering analysis...")
        
        # Select features for clustering
        clustering_features = [
            'Age', 'Salary', 'YearsAtCompany', 'JobSatisfaction',
            'PerformanceScore', 'OverallSatisfaction', 'WorkLifeBalance'
        ]
        
        # Filter available features
        available_clustering_features = [col for col in clustering_features if col in self.data.columns]
        
        # Prepare clustering data
        clustering_data = self.data[available_clustering_features].copy()
        clustering_data = clustering_data.fillna(clustering_data.median())
        
        # Scale data
        clustering_data_scaled = StandardScaler().fit_transform(clustering_data)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(clustering_data_scaled)
        
        # Add cluster labels to data
        self.data['Cluster'] = clusters
        
        # Analyze clusters
        cluster_analysis = self.data.groupby('Cluster')[available_clustering_features].mean()
        cluster_analysis['Count'] = self.data['Cluster'].value_counts().sort_index()
        
        print("Cluster Analysis:")
        print(cluster_analysis.round(2))
        
        # Visualize clusters using PCA
        pca = PCA(n_components=2)
        clustering_data_pca = pca.fit_transform(clustering_data_scaled)
        
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(clustering_data_pca[:, 0], clustering_data_pca[:, 1], 
                            c=clusters, cmap='viridis', alpha=0.6)
        plt.colorbar(scatter)
        plt.title('Employee Clusters (PCA Visualization)')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.tight_layout()
        plt.savefig('employee_clusters.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Employee clustering completed!")
        return cluster_analysis
    
    def attrition_risk_scoring(self):
        """Create comprehensive attrition risk scoring"""
        print("\n⚠️ Creating attrition risk scoring...")
        
        # Use the best model to predict attrition probability
        best_model_name = max(self.models.keys(), key=lambda x: self.models[x]['auc_score'])
        best_model = self.models[best_model_name]['model']
        
        # Predict probabilities for all employees
        if best_model_name == 'Logistic Regression':
            attrition_probs = best_model.predict_proba(self.scaler.transform(self.X))[:, 1]
        else:
            attrition_probs = best_model.predict_proba(self.X)[:, 1]
        
        # Create risk categories
        risk_categories = pd.cut(attrition_probs, 
                               bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
                               labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        
        # Add to data
        self.data['AttritionProbability'] = attrition_probs
        self.data['RiskCategory'] = risk_categories
        
        # Analyze risk distribution
        risk_analysis = self.data.groupby('RiskCategory').agg({
            'EmployeeID': 'count',
            'Salary': 'mean',
            'YearsAtCompany': 'mean',
            'JobSatisfaction': 'mean',
            'PerformanceScore': 'mean'
        }).round(2)
        
        risk_analysis.columns = ['EmployeeCount', 'AvgSalary', 'AvgTenure', 'AvgJobSatisfaction', 'AvgPerformance']
        
        print("Attrition Risk Analysis:")
        print(risk_analysis)
        
        # Save high-risk employees
        high_risk_employees = self.data[self.data['RiskCategory'].isin(['High', 'Very High'])].copy()
        high_risk_employees.to_csv('high_risk_employees.csv', index=False)
        
        print(f"✅ Risk scoring completed! {len(high_risk_employees)} high-risk employees identified.")
        return risk_analysis
    
    def create_advanced_insights(self):
        """Generate advanced business insights"""
        print("\n💡 Generating advanced business insights...")
        
        insights = {}
        
        # 1. High-risk employee characteristics
        high_risk = self.data[self.data['RiskCategory'] == 'Very High']
        if len(high_risk) > 0:
            insights['high_risk_avg_salary'] = high_risk['Salary'].mean()
            insights['high_risk_avg_tenure'] = high_risk['YearsAtCompany'].mean()
            insights['high_risk_avg_satisfaction'] = high_risk['JobSatisfaction'].mean()
        
        # 2. Performance vs. Satisfaction correlation
        if 'PerformanceScore' in self.data.columns and 'OverallSatisfaction' in self.data.columns:
            correlation = self.data['PerformanceScore'].corr(self.data['OverallSatisfaction'])
            insights['performance_satisfaction_correlation'] = correlation
        
        # 3. Salary vs. Attrition analysis
        salary_attrition = self.data.groupby('SalaryRange')['Attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        insights['highest_attrition_salary_range'] = salary_attrition.idxmax()
        insights['highest_attrition_salary_rate'] = salary_attrition.max()
        
        # 4. Department risk analysis
        dept_risk = self.data.groupby('Department')['AttritionProbability'].mean().sort_values(ascending=False)
        insights['highest_risk_department'] = dept_risk.index[0]
        insights['highest_risk_dept_probability'] = dept_risk.iloc[0]
        
        # 5. Training impact analysis
        if 'TrainingUtilization' in self.data.columns:
            training_impact = self.data.groupby('Attrition')['TrainingUtilization'].mean()
            insights['training_utilization_attrited'] = training_impact.get('Yes', 0)
            insights['training_utilization_retained'] = training_impact.get('No', 0)
        
        print("Advanced Insights:")
        for key, value in insights.items():
            if isinstance(value, float):
                print(f"  {key.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        
        return insights
    
    def export_ml_results(self):
        """Export machine learning results"""
        print("\n💾 Exporting machine learning results...")
        
        # Export predictions
        predictions_df = self.data[['EmployeeID', 'FirstName', 'LastName', 'Department', 
                                  'Attrition', 'AttritionProbability', 'RiskCategory']].copy()
        predictions_df.to_csv('attrition_predictions.csv', index=False)
        
        # Export cluster analysis
        cluster_df = self.data[['EmployeeID', 'FirstName', 'LastName', 'Department', 
                               'Cluster', 'Age', 'Salary', 'JobSatisfaction', 'PerformanceScore']].copy()
        cluster_df.to_csv('employee_clusters.csv', index=False)
        
        # Create ML report
        with open('ml_analysis_report.txt', 'w') as f:
            f.write("HR Analytics Machine Learning Report\n")
            f.write("=" * 40 + "\n\n")
            
            f.write("Model Performance:\n")
            for name, results in self.models.items():
                f.write(f"{name}:\n")
                f.write(f"  Accuracy: {results['accuracy']:.3f}\n")
                f.write(f"  AUC Score: {results['auc_score']:.3f}\n\n")
            
            f.write("Files Created:\n")
            f.write("- attrition_predictions.csv (Individual predictions)\n")
            f.write("- employee_clusters.csv (Cluster assignments)\n")
            f.write("- high_risk_employees.csv (High-risk employee list)\n")
            f.write("- feature_importance.png (Feature importance plot)\n")
            f.write("- employee_clusters.png (Cluster visualization)\n")
        
        print("✅ Machine learning results exported!")
        print("📁 Files created:")
        print("  - attrition_predictions.csv")
        print("  - employee_clusters.csv")
        print("  - high_risk_employees.csv")
        print("  - ml_analysis_report.txt")
    
    def run_advanced_analytics(self):
        """Run the complete advanced analytics pipeline"""
        print("🚀 Starting HR Advanced Analytics Pipeline")
        print("=" * 50)
        
        # Load data
        if not self.load_data():
            return False
        
        # Prepare data for ML
        self.prepare_attrition_data()
        
        # Train models
        self.train_attrition_models()
        
        # Feature importance
        self.feature_importance_analysis()
        
        # Clustering
        self.employee_clustering()
        
        # Risk scoring
        self.attrition_risk_scoring()
        
        # Advanced insights
        self.create_advanced_insights()
        
        # Export results
        self.export_ml_results()
        
        print("\n🎉 Advanced analytics pipeline completed successfully!")
        return True

# Main execution
if __name__ == "__main__":
    # Initialize advanced analytics
    analytics = HRAdvancedAnalytics()
    
    # Run the advanced analytics pipeline
    success = analytics.run_advanced_analytics()
    
    if success:
        print("\n📊 Advanced analytics completed!")
        print("Check the generated files for detailed insights and predictions.")
    else:
        print("\n❌ Advanced analytics failed. Please check your data file.") 