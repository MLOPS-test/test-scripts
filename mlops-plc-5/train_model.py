
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Load dataset "Churn_Modeling.csv" as pandas dataframe
df = pd.read_csv("Churn_Modeling.csv")
df.head()


# Define target variable and features
X = df[["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "IsActiveMember", "EstimatedSalary"]].copy()
y = df[["Exited"]]


# Handling category labels present in `Geography` and `Gender` columns
# Get the distinct categories present in each categorical column
# YOUR CODE HERE..

# Create dictionaries to map categorical values to numberic labels. OR Use LabelEncoder
# YOUR CODE HERE..

# Map categorical values to numberic labels using respective dictionaries
# YOUR CODE HERE..

# Split data into training (80%) and test (20%) sets
# Use random_state and stratify parameters
# YOUR CODE HERE

# Save training and test sets into `data/train.csv` & `data/test.csv`
# YOUR CODE HERE..
# YOUR CODE HERE..


# Model Training
# Create Random Forest Classifier model with n_estimators=100, and fit it on the training set
# YOUR CODE HERE..

# Evaluate the model performance(accuracy score) on test set
# YOUR CODE HERE..


# Save Actual and Predicted labels for test set into `model/predictions.csv`
# Hint: Create a dataframe having actual and predictes labels as columns, then save it to the csv file.
# YOUR CODE HERE..


# Save the trained model as pickle file `model/my_model.pkl`
# YOUR CODE HERE


###################  MLflow related code below  ###############################

# import mlflow

# Start mlflow run
# mlflow.start_run()

# Log parameter `n_estimator`
# YOUR CODE HERE

# Log metric `accuracy`
# YOUR CODE HERE

# Log artifacts - `data/train.csv`, `data/test.csv`, and `model/predictions.csv`
# YOUR CODE HERE...

# Log model
# YOUR CODE HERE

# End mlflow run
# mlflow.end_run()
