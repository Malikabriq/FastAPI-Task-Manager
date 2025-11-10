import os, json

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "tasks.json")

def ensure_data_dir():
    d = os.path.dirname(DATA_FILE)
    os.makedirs(d, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def load_data():
    ensure_data_dir()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
