import sys
sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-
import pandas as pd
import re
from playwright.sync_api import sync_playwright
import sqlite3


class BusRouteInfo:
    def __init__(self, routeid: str, direction: str = 'go'):
        self.rid = routeid
        self.content = None
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}'

        if direction not in ['go', 'come']:
            raise ValueError("Direction must be 'go' or 'come'")

        self.direction = direction

        self._fetch_content()
    

    def _fetch_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)
            
            if self.direction == 'come':
                page.click('a.stationlist-come-go-gray.stationlist-come')
            
            page.wait_for_timeout(3000)  # wait for 1 second
            self.content = page.content()
            browser.close()


        # Write the rendered HTML to a file route_{rid}.html
        with open(f"data/ebus_taipei_{self.rid}.html", "w", encoding="utf-8") as file:
            file.write(self.content)
from bs4 import BeautifulSoup
import csv
import os


class BusRouteInfo:
    def __init__(self, routeid: str, direction: str = 'go'):
        self.rid = routeid
        self.content = None
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}'

        if direction not in ['go', 'come']:
            raise ValueError("Direction must be 'go' or 'come'")
        self.direction = direction

        self._fetch_content()

    def _fetch_content(self):
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)

            if self.direction == 'come':
                page.click('a.stationlist-come-go-gray.stationlist-come')

            page.wait_for_timeout(3000)
            self.content = page.content()
            browser.close()

        os.makedirs("data", exist_ok=True)
        with open(f"data/ebus_taipei_{self.rid}.html", "w", encoding="utf-8") as file:
            file.write(self.content)

    def parse_and_export_csv(self, output_csv: str = None):
        soup = BeautifulSoup(self.content, 'html.parser')
        stop_blocks = soup.select('.stop-info')

        result = []
        for index, block in enumerate(stop_blocks, start=1):
            arrival_info = block.select_one('.estimate-time').text.strip()
            stop_name = block.select_one('.stopname-zh').text.strip()
            stop_id = block.get('data-stopid')
            lat = block.get('data-latitude')
            lng = block.get('data-longitude')

            result.append([
                arrival_info,
                index,
                stop_name,
                stop_id,
                lat,
                lng
            ])

        output_csv = output_csv or f"data/bus_route_{self.rid}_{self.direction}.csv"
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in result:
                writer.writerow(row)

        print(f"[INFO] CSV 匯出成功：{output_csv}")


# 範例用法
if __name__ == "__main__":
    routeid = input("請輸入公車路線代碼（如 0100000A00）：")
    direction = input("請輸入方向（go 或 come，預設為 go）：").strip() or "go"
    bus = BusRouteInfo(routeid, direction)
    bus.parse_and_export_csv()

