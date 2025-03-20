
import yaml
from pathlib import Path
filepath = Path(__file__)
root = filepath.parent
#root = filepath.parents[1]

# Initial score
score = 0

# Check for saved train.csv and test.csv
train_file = Path(str(root) + "/" + "data/train.csv")
test_file = Path(str(root) + "/" + "data/test.csv")

if train_file.is_file():
    score += 3
    print("Score given for creating train csv: 3")
if test_file.is_file():
    score += 2
    print("Score given for creating test csv: 2")

# Check for saved model and predictions.csv
pred_file = Path(str(root) + "/" + "model/predictions.csv")
model_path = Path(str(root) + "/" + "model")

if pred_file.is_file():
    score += 2
    print("Score given for creating predictions csv: 2")

for file in model_path.iterdir():
    if file.is_file() and file.suffix == '.pkl':
        score += 3
        print("Score given for saving model pkl: 3")


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

    run_path = exp_dict[max(exp_dict.keys())]
    #print("run path:", run_path)
    
    # Check the run folder for logged params, metrics, artifacts
    for subdir in run_path.iterdir():
        if subdir.is_dir():
            if subdir.name == 'params':
                if any(subdir.iterdir()):     # if directory is not empty
                    score += 2
                    print("Score given for logging n_estimator param with mlflow: 2")
            if subdir.name == 'metrics': 
                if any(subdir.iterdir()):     # if directory is not empty
                    score += 2
                    print("Score given for logging accuracy metric with mlflow: 2")
            if subdir.name == 'artifacts':    # if directory is not empty
                if any(subdir.iterdir()):
                    for artifact_file in subdir.iterdir():
                        if artifact_file.is_file() and artifact_file.suffix == '.csv':      # check for logged CSVs
                            #print("score added for ", artifact_file.name)
                            score += 1
                            print(f"Score given for logging {artifact_file.name} csv with mlflow: 1")
                        if artifact_file.is_dir():
                            for sub_art_file in artifact_file.iterdir():
                                if sub_art_file.is_file() and sub_art_file.suffix == '.pkl':  # check for logged model
                                    score += 3
                                    print("Score given for logging model pkl with mlflow: 3")

if score < 0:
    score_pct = 0
elif score > 20:
    score_pct = 100
else:
    score_pct = (score / 20) * 100

print(f"Score given for challenge: {score}/20")
print(f"Partial Credit: {score_pct}%")
