# fake_eta.py
import json

def load_eta_data(filename="sample_eta.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def get_eta(route_name, direction, stop_name):
    data = load_eta_data()
    return data.get(route_name, {}).get(direction, {}).get(stop_name, "無資料")
