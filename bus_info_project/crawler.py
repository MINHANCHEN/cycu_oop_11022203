from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

# 啟動瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 不開啟視窗
driver = webdriver.Chrome(service=Service("./chromedriver"), options=options)

def get_bus_eta(route_name):
    url = "https://ebus.gov.taipei/ebus"
    driver.get(url)
    time.sleep(2)  # 等待頁面載入

    # 點選「路線查詢」
    route_button = driver.find_element(By.LINK_TEXT, "路線查詢")
    route_button.click()
    time.sleep(2)

    # 找到輸入框，輸入路線名稱（例如 "278"）
    input_box = driver.find_element(By.ID, "RouteSearch")
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

# 範例：查詢 278 路線
get_bus_eta("278")

driver.quit()
