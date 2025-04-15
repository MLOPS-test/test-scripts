from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Create a FastAPI object `app`
app = FastAPI()

# Load model and encoders
rf_model = joblib.load("trained_model/rf_model_term_deposit.pkl")
label_encoders = joblib.load("trained_model/label_encoders.pkl")

# Define request schema
class TermDepositInput(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    default: int
    balance: float
    housing: int
    loan: int
    day_of_week: str
    month: str
    duration: int
    campaign: int
    pdays: int
    previous: int

# Function to preprocess data before feeding to model
def preprocess_input(data: TermDepositInput):
    input_dict = data.dict()
    # Encode categorical features
    for col in ['job', 'marital', 'education', 'day_of_week', 'month']:
        le = label_encoders[col]
        value = input_dict[col]
        if value in le.classes_:
            input_dict[col] = le.transform([value])[0]
        else:
            input_dict[col] = 0  # fallback
    return pd.DataFrame([input_dict])


# Create a POST endpoint `/predict` that should take input the data of type `TermDepositInput` via request body,
# and return the prediction response in a JSON format. For example: `{"prediction": "Subscribed (y=1)"}`
# The data must be processed using `preprocess_input()` function before feeding to the model for prediction.
# Output should be either of the below: 
# {"prediction": "Subscribed (y=1)"} or 
# {"prediction": "Not Subscribed (y=0)"}

@app.post("/predict")
def predict_deposit(data: TermDepositInput):
    # YOUR CODE HERE...
    result = "Update this variable"
    return {"prediction": result}


if __name__ == "__main__":
    # Webserver -> Uvicorn
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
