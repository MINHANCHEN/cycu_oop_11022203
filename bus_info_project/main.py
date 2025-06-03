import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

class BusRouteFinder:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def find_routes(self, origin, destination):
        results = []
        for (route_name, direction), group in self.df.groupby(['route_name', 'direction_text']):
            stops = group.sort_values('stop_number')['stop_name'].tolist()
            if origin in stops and destination in stops:
                if stops.index(origin) < stops.index(destination):
                    results.append({
                        'route_name': route_name,
                        'direction_text': direction,
                        'stops': stops[stops.index(origin):stops.index(destination)+1]
                    })
        return results

def get_bus_eta(route_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
    url = "https://ebus.gov.taipei/ebus"
    driver.get(url)
    time.sleep(2)

    # 點選「路線查詢」
    try:
        route_button = driver.find_element(By.LINK_TEXT, "路線查詢")
        route_button.click()
        time.sleep(2)

        # 找到輸入框，輸入路線名稱
        input_box = driver.find_element(By.ID, "RouteSearch")
        input_box.clear()
        input_box.send_keys(route_name)
        time.sleep(1)

        # 模擬按下查詢
        search_button = driver.find_element(By.ID, "btnRouteSearch")
        search_button.click()
        time.sleep(3)

        # 抓下查詢結果
        soup = BeautifulSoup(driver.page_source, "html.parser")
        result_area = soup.find("div", id="routeResult")

        if result_area:
            print(result_area.text.strip())
        else:
            print("❌ 查無資料或格式變更")
    except Exception as e:
        print(f"❌ 查詢過程發生錯誤：{e}")
    finally:
        driver.quit()

def main():
    finder = BusRouteFinder("HW2.csv")
    print("🚌 歡迎使用台北市公車查詢系統")
    origin = input("請輸入出發站（中文）：").strip()
    destination = input("請輸入目的站（中文）：").strip()

    routes = finder.find_routes(origin, destination)

    if not routes:
        print("❌ 找不到符合的路線。請確認站名是否正確，且目的站應在出發站之後。")
        return

    for route in routes:
        route_name = route['route_name']
        direction = route['direction_text']
        stops = route['stops']

        print(f"\n🚌 路線：{route_name}（{direction}）")
        print(f"經過站：{' → '.join(stops)}")
        print("即時動態查詢結果：")
        get_bus_eta(route_name)
        print("-" * 40)

if __name__ == "__main__":
    main()