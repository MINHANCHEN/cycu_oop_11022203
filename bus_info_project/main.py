import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class BusRouteFinder:
    def __init__(self, csv_file):
        """初始化，讀取靜態資料 (HW2.csv)"""
        self.df = pd.read_csv(csv_file)

    def find_routes(self, origin, destination):
        """尋找包含出發站與目的站的有效路線"""
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

def get_bus_eta(route_name, direction):
    """使用 Playwright 爬取即時到站資訊"""
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_name}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()
        page.goto(url)

        try:
            # 切換方向（去程或回程）
            if direction == "come":
                page.click('a.stationlist-come-go-gray.stationlist-come')

            # 等待目標元素加載
            page.wait_for_selector("li.auto-list-stationlist", timeout=10000)

            # 抓取查詢結果
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            stops = soup.find_all("li", class_="auto-list-stationlist")

            if not stops:
                return "❌ 查無資料或格式變更"

            # 解析站牌資訊
            results = []
            for stop in stops:
                stop_name = stop.find("span", class_="auto-list-stationlist-place").text.strip()
                arrival_info = stop.find("span", class_="auto-list-stationlist-position").text.strip()
                results.append(f"{stop_name} - {arrival_info}")

            return "\n".join(results)
        except Exception as e:
            return f"❌ 查詢過程發生錯誤：{e}"
        finally:
            browser.close()

def main():
    """主程式入口"""
    finder = BusRouteFinder("HW2.csv")
    print("🚌 歡迎使用台北市公車查詢系統")
    origin = input("請輸入出發站（中文）：").strip()
    destination = input("請輸入目的站（中文）：").strip()

    # 1️⃣ 找出包含出發站與目的站的有效路線
    routes = finder.find_routes(origin, destination)

    if not routes:
        print("❌ 找不到符合的路線。請確認站名是否正確，且目的站應在出發站之後。")
        return

    # 2️⃣ 顯示路線資訊並爬取即時動態
    for route in routes:
        route_name = route['route_name']
        direction = route['direction_text']
        stops = route['stops']

        print(f"\n🚌 路線：{route_name}（{direction}）")
        print(f"經過站：{' → '.join(stops)}")
        print("即時動態查詢結果：")
        eta_info = get_bus_eta(route_name, "go")  # 預設為去程
        print(eta_info)
        print("-" * 40)

if __name__ == "__main__":
    main()