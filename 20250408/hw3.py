import requests
import csv

def fetch_and_export_bus_stops(route_id):
    """
    根據輸入的公車代碼，從臺北市公車公開 API 抓取資料並輸出為 CSV 檔案。
    
    :param route_id: 公車代碼（例如 '0100000A00'）
    """
    # API URL
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"

    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 若有錯誤，將引發例外

        data = response.json()

        if not data:
            print("⚠️ 找不到資料，請確認路線代碼是否正確。")
            return

        # 準備 CSV 檔案名稱
        csv_filename = f"bus_stops_{route_id}.csv"

        # 開始寫入 CSV
        with open(csv_filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            # 寫入欄位名稱
            writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])

            for direction in data:
                stops = direction.get("Stops", [])
                for stop in stops:
                    arrival_info = stop.get("EstimateTime", "進站中")  # 假設 EstimateTime 為到站時間
                    stop_number = stop.get("SequenceNo", "")
                    stop_name = stop.get("StopName", {}).get("Zh_tw", "")
                    stop_id = stop.get("StopID", "")
                    latitude = stop.get("StopPosition", {}).get("PositionLat", "")
                    longitude = stop.get("StopPosition", {}).get("PositionLon", "")

                    writer.writerow([
                        arrival_info,
                        stop_number,
                        stop_name,
                        stop_id,
                        latitude,
                        longitude
                    ])

        print(f"✅ 資料已成功儲存為 {csv_filename}")

    except requests.exceptions.RequestException as e:
        print(f"❌ 網路錯誤：{e}")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

# 範例使用方式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼（例如 0100000A00）：")
    fetch_and_export_bus_stops(route_id)

