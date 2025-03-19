
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Load dataset as pandas dataframe
df = pd.read_csv("Churn_Modeling.csv")
df.head()


# Define target variable and features
X = df[["CreditScore", "Geography", "Gender", "Age", "Tenure", "Balance", "NumOfProducts", "IsActiveMember", "EstimatedSalary"]].copy()
y = df[["Exited"]]


# Handling category labels present in `Geography` and `Gender` columns
# Get the distinct categories present in each categorical column
# print(X['Geography'].unique())
# print(X['Gender'].unique())

# Create dictionaries to map categorical values to numberic labels. OR Use LabelEncoder
geography_mapping = {'France': 0, 'Spain': 1, 'Germany': 2}
gender_mapping = {'Female': 0, 'Male': 1}

# Map categorical values to numbers using respective dictionaries
X['Geography'] = X['Geography'].map(geography_mapping)
X['Gender'] = X['Gender'].map(gender_mapping)

# Split data into training (80%) and test (20%) sets
# Use random_state and stratify parameters
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3, stratify=y)

# Save training and test sets as train.csv & test.csv inside data/ directory
train_data = X_train.copy()
train_data["Exited"] = y_train

test_data = X_test.copy()
test_data["Exited"] = y_test

train_data.to_csv('data/train.csv', index=False)
test_data.to_csv('data/test.csv', index=False)


# Model Training
# Create Random Forest Classifier model with n_estimators=100
rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_train, y_train.values.ravel())

# Evaluate the model performance on test set
y_pred = rf_model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc}")


# Save Actual and Predicted labels for test set into `model/predictions.csv`
pred_data = pd.DataFrame({'Actual': y_test.values.ravel(),
                          'Predicted': y_pred})
pred_data.to_csv("model/predictions.csv", index=False)


# Save model as pickle file inside model/ directory
joblib.dump(rf_model, "model/my_model.pkl")
print("Model saved successfully!")


###################  MLflow related code below  ###############################

import mlflow

# Start mlflow run
mlflow.start_run()

# Log parameter `n_estimator`
mlflow.log_param("n_estimator", 100)

# Log metric `accuracy`
mlflow.log_metric("accuracy", acc)

# Log artifacts - `data/train.csv`, `data/test.csv`, and `model/predictions.csv`
mlflow.log_artifact("data/train.csv")
mlflow.log_artifact("data/test.csv")
mlflow.log_artifact("model/predictions.csv")

# Log model
mlflow.sklearn.log_model(rf_model, "random_forest_model")

# End mlflow run
mlflow.end_run()

