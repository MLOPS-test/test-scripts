import sys
from pathlib import Path
filepath = Path(__file__)
sys.path.append(str(filepath.parents[1]))

from sklearn.metrics import accuracy_score


def test_model_accuracy():
    # ADD YOUR TEST CASE to check for model test accuracy > 0.8
    assert False  # <-- ADD YOUR ASSERT STATEMENT and remove `False``

def test_make_prediction_function():
    # ADD YOUR TEST CASE to check the output from make_prediction(), should be either "Subscribed (y=1)", or "Not Subscribed (y=0)"
    assert False  # <-- ADD YOUR ASSERT STATEMENT and remove `False``

