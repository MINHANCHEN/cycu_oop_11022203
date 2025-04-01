import sys
import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

# 設定 Python 終端輸出為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 發送 GET 請求
response = requests.get(url, headers=headers)

# 確保請求成功
if response.status_code == 200:
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # 顯示完整 HTML（避免 UnicodeEncodeError）
    print(soup.prettify())

    # 找到所有表格
    tables = soup.find_all("table")

    # 初始化 DataFrame 列表
    dataframes = []

    # 遍歷表格
    for table in tables:
        rows = []
        for tr in table.find_all("tr", class_=["ttego1", "ttego2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())
                stop_link = td.find("a")["href"] if td.find("a") else None
                rows.append({"站點名稱": stop_name, "連結": stop_link})
        
        if rows:
            df = pd.DataFrame(rows)
            dataframes.append(df)

    if len(dataframes) >= 2:
        df1, df2 = dataframes[0], dataframes[1]
        print("第一個 DataFrame:")
        print(df1)
        print("\n第二個 DataFrame:")
        print(df2)
    else:
        print("未找到足夠的表格資料。")

else:
    print(f"❌ 無法下載網頁，HTTP 狀態碼: {response.status_code}")
