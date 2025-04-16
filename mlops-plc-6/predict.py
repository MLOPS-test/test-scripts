import pandas as pd
import joblib

## Load trained model
# rf_model = # YOUR CODE HERE to load the model from path "trained_model/rf_model_term_deposit.pkl"


# Load label encoders
label_encoders = joblib.load("trained_model/label_encoders.pkl")


sample_input = {
    'age': 33,
    'job': 'technician',
    'marital': 'single',
    'education': 'secondary',
    'default': 0,
    'balance': 1500,
    'housing': 1,
    'loan': 0,
    'day_of_week': 'mon',
    'month': 'may',
    'duration': 120,
    'campaign': 2,
    'pdays': -1,
    'previous': 0
}

# Apply label encoding
encoded_input = sample_input.copy()
for col in ['job', 'marital', 'education', 'day_of_week', 'month']:
    le = label_encoders[col]
    encoded_input[col] = le.transform([sample_input[col]])[0] if sample_input[col] in le.classes_ else 0  # fallback

# Convert to DataFrame
sample_input_df = pd.DataFrame(encoded_input, index=[0])

# Inference function
def make_prediction(input_df):
    prediction = rf_model.predict(input_df)[0]
    # YOUR CODE HERE to return "Subscribe (y=1)" if prediction == 1 else "Not Subscribe (y=0)"


if __name__ == "__main__":
    pred = make_prediction(sample_input_df)
    print(pred)
