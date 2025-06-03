import pandas as pd
import json

# 讀取你的 HW2.csv
df = pd.read_csv("HW2.csv", encoding="utf-8")

# 準備假資料
sample_eta = {}
grouped = df.groupby(['route_name', 'direction_text'])

for (route_name, direction_text), group in grouped:
    sorted_group = group.sort_values("stop_number")
    stop_names = sorted_group['stop_name'].tolist()

    selected_stops = stop_names[:3]  # 選前三站
    eta_times = [2, 5, 9]            # 模擬時間

    if route_name not in sample_eta:
        sample_eta[route_name] = {}
    sample_eta[route_name][direction_text] = {
        stop: f"{eta} 分鐘" for stop, eta in zip(selected_stops, eta_times)
    }

# 儲存為 JSON 檔案
with open("sample_eta.json", "w", encoding="utf-8") as f:
    json.dump(sample_eta, f, ensure_ascii=False, indent=2)

print("✅ 模擬即時資料已儲存到 sample_eta.json")
