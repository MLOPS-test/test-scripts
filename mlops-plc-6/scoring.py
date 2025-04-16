
# While attempting the test, DO NOT EDIT this file. It may result in 0 score.

import os
import subprocess
import requests
import yaml
from pathlib import Path
filepath = Path(__file__)
root = filepath.parent
#root = filepath.parents[1]

# Initial score
score = 0

print("--------- Preprocess the Data (`data_preprocessing.py`) [2 Marks] ---------")

# Data preprocessing points
try:
    from data_preprocessing import X_train, X_test, y_train, y_test
    score += 1
    print("Points given for train-test-split step: 1")
except:
    print("[ERROR]: `from data_preprocessing import X_train, X_test, y_train, y_test` <-- NOT WORKING")
    pass

# Check for saved `label_encoders.pkl` & `rf_model_term_deposit.pkl`
encoder_file = Path(str(root) + "/" + "trained_model/label_encoders.pkl")

if encoder_file.is_file():
    score += 1
    print("Points given for saving label_encoders.pkl: 1")
else:
    print("[ERROR]: `trained_model/label_encoders.pkl` <-- FILE DOES NOT EXIST")

print("\n--------- Train a Machine Learning Model (`train_model.py`) [4 Marks] ---------")

model_file = Path(str(root) + "/" + "trained_model/rf_model_term_deposit.pkl")

if model_file.is_file():
    score += 1
    print("Points given for saving rf_model_term_deposit.pkl: 1")
else:
    print("[ERROR]: `trained_model/rf_model_term_deposit.pkl` <-- FILE DOES NOT EXIST")


# Check for logged parameter in mlflow
exp_path = Path(str(root) + "/" + "mlruns/0")

if exp_path.exists():      # if mlruns/0 exists

    exp_dict = {}

    for subpath in exp_path.iterdir():         # 0/*
        if subpath.is_dir():
            for subdir in subpath.iterdir():
                if subdir.is_file():              # 0/*/meta.yaml
                    # Load the YAML file
                    with open(subdir, 'r') as file:
                        data = yaml.safe_load(file)
                        start_time = data['start_time']
                        exp_dict[start_time] = subpath
                        # print(subpath, start_time)

    run_path = exp_dict[max(exp_dict.keys())]      # latest run
    #print("run path:", run_path)
    
    # Check the run folder for logged params, metrics, artifacts
    for subdir in run_path.iterdir():
        if subdir.is_dir():
            if subdir.name == 'params':
                if any(subdir.iterdir()):     # if directory is not empty
                    score += 1
                    print("Points given for logging parameters with mlflow: 1")
                else:
                    print("[ERROR]: Parameters NOT LOGGED with MLflow")
            if subdir.name == 'metrics': 
                if any(subdir.iterdir()):     # if directory is not empty
                    score += 1
                    print("Points given for logging metrics with mlflow: 1")
                else:
                    print("[ERROR]: Metrics NOT LOGGED with MLflow")
            if subdir.name == 'artifacts':    # if directory is not empty
                if any(subdir.iterdir()):
                    for artifact_file in subdir.iterdir():
                        if artifact_file.is_dir():
                            for sub_art_file in artifact_file.iterdir():
                                if sub_art_file.is_file() and sub_art_file.suffix == '.pkl':  # check for logged model
                                    score += 1
                                    print("Points given for logging model pkl with mlflow: 1")
                else:
                    print("[ERROR]: Model NOT LOGGED with MLflow")

else:
    print("[ERROR]: LOGGING with MLflow NOT IMPLEMENTED")


# Evaluate Inference - predict.py
print("\n--------- Make Predictions - Inference (`predict.py`) [2 Marks] ---------")

# Check for `predict.py`
try:
    from predict import rf_model
    score += 1
    print("Points given for loading the model pkl: 1")
except:
    pass
    print("[ERROR]: Model not loaded in predict.py")

try:
    from predict import make_prediction, sample_input_df
    sample_pred = make_prediction(sample_input_df)
    if sample_pred in ["Subscribed (y=1)", "Not Subscribed (y=0)"]:
        score += 1
        print("Points given for make_prediction() func: 1")
except:
    pass
    print("[ERROR]: make_prediction() function not completed in predict.py")


# Evaluate pytest tests
print("\n--------- Build Test Cases (`test/test_prediction.py`) [4 Marks] ---------")

# Check for test_model_accuracy() test case:
try:
    result = subprocess.run(['python3', '-m', 'pytest', 'tests/test_prediction.py::test_model_accuracy'], capture_output=True, text=True)
    #print(result.stdout)
    #print(result.stderr)
    if result.returncode == 0:
        score += 2
        print("Points given for test_model_accuracy() func: 2")
    else:
        print("[ERROR]: `test_model_accuracy()` <-- TEST FAILED or NOT DEFINED YET")
except Exception as e:
    print(f"[ERROR]: Error running pytest: {e}")


# Check for test_make_prediction() test case:
try:
    result = subprocess.run(['python3', '-m', 'pytest', 'tests/test_prediction.py::test_make_prediction_function'], capture_output=True, text=True)
    #print(result.stdout)
    #print(result.stderr)
    if result.returncode == 0:
        score += 2
        print("Points given for test_make_prediction_function() func: 2")
    else:
        print("[ERROR]: `test_make_prediction_function()` <-- TEST FAILED or NOT DEFINED YET")
except Exception as e:
    print(f"[ERROR]: Error running pytest: {e}")


# Serve the Model via REST API using FastAPI (`app.py`) [4 Marks]
print("\n--------- Serve the Model via REST API using FastAPI (`app.py`) [4 Marks] ---------")

try:
    install_httpx = subprocess.run(['pip', 'install', 'httpx'], capture_output=True, text=True)
    # test_app.py  `pip install httpx`
    from fastapi.testclient import TestClient
    from app import app

    client = TestClient(app)

    payload = {
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

    response = client.post("/predict", json=payload)

    if response.json()["prediction"] in ["Subscribed (y=1)", "Not Subscribed (y=0)"]:
        score += 4
        print("Points given for FastAPI implementation: 4")
    elif response.json()["prediction"] == "Update this variable":
        print("[ERROR]: `app.py` <-- FastAPI part NOT IMPLEMENTED YET")
    else:
        print("[ERROR]: Error in FastAPI implementation `app.py`")

except Exception as e:
    print("[ERROR]: Error in FastAPI implementation `app.py`. ", e)
    pass


# Dockerize the FastAPI Application [4 Marks]
print("\n--------- Dockerize the FastAPI Application [4 Marks] ---------")


# Define the required Dockerfile keywords (some are alternatives)
REQUIRED_KEYWORDS = {
    "FROM": False,
    "ADD_OR_COPY": False,
    "RUN": False,
    "CMD_OR_ENTRYPOINT": False,
}

def check_dockerfile(path="Dockerfile"):
    global score
    if not os.path.isfile(path):
        print(f"[ERROR]: Dockerfile not found at: /{path}")
        return

    with open(path, "r") as file:
        lines = file.readlines()

    for line in lines:
        stripped = line.strip().upper()
        if stripped.startswith("FROM"):
            REQUIRED_KEYWORDS["FROM"] = True
        elif stripped.startswith("ADD") or stripped.startswith("COPY"):
            REQUIRED_KEYWORDS["ADD_OR_COPY"] = True
        elif stripped.startswith("RUN"):
            REQUIRED_KEYWORDS["RUN"] = True
        elif stripped.startswith("CMD") or stripped.startswith("ENTRYPOINT"):
            REQUIRED_KEYWORDS["CMD_OR_ENTRYPOINT"] = True

    # Dockerfile Keyword Check:
    sub_score = 0
    for keyword, found in REQUIRED_KEYWORDS.items():
        if found:
            sub_score += 0.5
        # status = "Found" if found else "Missing"
        # print(f"{keyword}: {status}")
    if sub_score == 0:
        print("[ERROR]: Dockerfile does not implemented correctly")
    else:
        score += sub_score
        print(f"Points given for Dockerfile: {sub_score}")

check_dockerfile()


# Check Docker Image
try:
    result = subprocess.run(['docker', 'images', '-q'], capture_output=True, text=True)
    output = result.stdout.strip()
    if output:
        score += 1
        print(f"Points given for building Docker image: 1")
    else:
        print("[ERROR]: Docker image NOT BUILT YET")
except Exception as e:
    print(f"[ERROR]: Error running `docker images -q` command: {e}")


# Check Docker Container if running successfully

def check_container():
    global score
    # Build the Docker image
    #print("Building Docker image...")
    try:
        result = subprocess.run(['docker', 'build', '-t', 'diamond-clubs', '.'], capture_output=True, text=True)
        #print(result.stdout)
        #print(result.stderr)
        if result.returncode != 0:
            print("[ERROR]: Docker build failed.")
            return
    except Exception as e:
        print(f"[ERROR]: Error building Docker image: {e}")
        return

    # Run the Docker container
    #print("Running Docker container...")
    try:
        container = subprocess.Popen(['docker', 'run', '-d', '-p', '8080:8080', 'diamond-clubs'], stdout=subprocess.PIPE)
        container_id = container.stdout.read().strip().decode('utf-8')
        #print(f"Container started with ID: {container_id}")
    except Exception as e:
        print(f"[ERROR]: Error running Docker container: {e}")
        return

    # Wait for a moment to ensure the server is up
    import time
    time.sleep(5)

    # Test the FastAPI endpoint
    #print("Testing FastAPI endpoint...")
    try:
        payload = {
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
        response = requests.post('http://localhost:8080/predict', json=payload)

        if response.json()["prediction"] in ["Subscribed (y=1)", "Not Subscribed (y=0)"]:
            score += 1
            print("Points given for successfully running application in docker container: 1")
        elif response.json()["prediction"] == "Update this variable":
            print("[ERROR]: `app.py` <-- FastAPI part NOT IMPLEMENTED YET")
        else:
            print("[ERROR]: Error in FastAPI implementation `app.py`")
    except Exception as e:
        print(f"[ERROR]: Error testing FastAPI endpoint running in container: {e}")
    finally:
        # Stop and remove the Docker container
        _ = subprocess.run(['docker', 'stop', container_id], capture_output=True, text=True)
        _ = subprocess.run(['docker', 'rm', container_id], capture_output=True, text=True)


check_container()


if score < 0:
    score_pct = 0
elif score > 20:
    score_pct = 100
else:
    score_pct = (score / 20) * 100

print("------------------------")
print(f"Score given for challenge: {score}/20")
print(f"Partial Credit: {score_pct}%")
