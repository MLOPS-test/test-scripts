
import requests

def check_fastapi_endpoint():
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

        if response.json()["prediction"] in ["Subscribe (y=1)", "Not Subscribe (y=0)"]:
            print("Application running fine:")
            print(f"Output: {response.json()}")
        elif response.json()["prediction"] == "Update this variable":
            print("[ERROR]: `app.py` <-- FastAPI part NOT IMPLEMENTED YET")
        else:
            print("[ERROR]: Error in FastAPI implementation `app.py`")
    except Exception as e:
        print(f"[ERROR]: Error testing FastAPI endpoint. May be the app.py is not running. \n{e}")
    finally:
        pass


if __name__ == "__main__":
    check_fastapi_endpoint()
