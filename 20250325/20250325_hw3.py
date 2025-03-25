import requests
from bs4 import BeautifulSoup

# 設定網址和 headers
base_url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

def search_bus_station(bus_station_name):
    # 根據站名建立搜尋參數
    params = {
        'station': bus_station_name
    }

    # 發送 GET 請求
    response = requests.get(base_url, params=params)

    # 檢查請求是否成功
    if response.status_code != 200:
        print("Error: Unable to fetch data.")
        return

    # 解析頁面內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 根據頁面結構提取資料
    # 這部分會依據網站的 HTML 結構而有所不同
    # 假設有一個 <table> 顯示公車路線，我們可以抓取表格中的資料
    table = soup.find('table')
    if table:
        rows = table.find_all('tr')

        # 遍歷表格中的每一行，打印出相關資料
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 1:
                # 假設每一列中有需要的路線資訊
                bus_route = columns[0].text.strip()  # 公車路線
                stop_name = columns[1].text.strip()  # 站點名稱
                print(f"Route: {bus_route}, Stop: {stop_name}")
    else:
        print("No bus information found for this station.")

# 主程式，讓用戶輸入站點
if __name__ == "__main__":
    bus_station_name = input("Enter the bus station name: ")
    search_bus_station(bus_station_name)
