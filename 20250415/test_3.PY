import sys
sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
import requests
import csv
import os


class BusRouteInfo:
    def __init__(self, routeid: str):
        self.rid = routeid
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={self.rid}'
        self.data = self._fetch_content()

    def _fetch_content(self):
        response = requests.get(self.url)
        print(f"API 回應狀態碼: {response.status_code}")
        print(f"API 回應內容: {response.text}")  # 印出回應內容

        if response.status_code != 200:
            raise Exception(f"無法取得資料，狀態碼：{response.status_code}")

        if not response.text.strip():
            raise Exception("API 回應為空，請確認路線代碼是否正確。")

        try:
            return response.json()
        except ValueError:
            raise Exception(f"回應不是有效的 JSON 格式：{response.text}")

    def parse_and_export_csv(self, output_csv: str = None):
        os.makedirs("data", exist_ok=True)
        output_csv = output_csv or f"data/bus_route_{self.rid}.csv"

        result = []

        for direction in self.data:
            stops = direction.get('Stops', [])
            for stop in stops:
                stop_number = stop.get('Sequence', '')
                stop_name = stop.get('StopName', {}).get('Zh_tw', '')
                stop_id = stop.get('StopID', '')
                lat = stop.get('StopPosition', {}).get('PositionLat', '')
                lng = stop.get('StopPosition', {}).get('PositionLon', '')
                est_sec = stop.get('EstimateTime', None)

                if est_sec is None:
                    arrival_info = "進站中"
                else:
                    arrival_info = f"{est_sec // 60}分鐘"

                result.append([
                    arrival_info,
                    stop_number,
                    stop_name,
                    stop_id,
                    lat,
                    lng
                ])

        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["公車到達時間", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])
            for row in result:
                writer.writerow(row)

        print(f"[INFO] CSV 匯出成功：{output_csv}")


# 範例用法
if __name__ == "__main__":
    routeid = input("請輸入公車路線代碼（如 0100000A00）：").strip()
    try:
        bus = BusRouteInfo(routeid)
        bus.parse_and_export_csv()
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
