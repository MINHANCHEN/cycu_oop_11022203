# main.py
import pandas as pd
from crawler.ebus_route_info import taipei_route_info

CSV_PATH = 'data/HW2.csv'

def load_static_data():
    """讀取靜態資料 (HW2.csv)"""
    df = pd.read_csv(CSV_PATH)
    df['stop_name'] = df['stop_name'].str.strip().str.lower()  # 去除空格並轉為小寫
    return df

def find_valid_routes(df, start_station, end_station):
    """尋找包含出發站與目的站的有效路線"""
    matched_routes = []

    # 檢查站名是否存在於資料中
    if start_station not in df['stop_name'].values:
        print(f"⚠️ 出發站 '{start_station}' 不存在於資料中。")
        return matched_routes
    if end_station not in df['stop_name'].values:
        print(f"⚠️ 目的站 '{end_station}' 不存在於資料中。")
        return matched_routes

    for route_name in df['route_name'].unique():  # 使用正確的欄位名稱
        sub_df = df[df['route_name'] == route_name]
        try:
            # 找到出發站與目的站的索引
            start_idx = sub_df[sub_df['stop_name'] == start_station].index[0]
            end_idx = sub_df[sub_df['stop_name'] == end_station].index[0]
            if start_idx < end_idx:  # 確保出發站在目的站之前
                matched_routes.append(route_name)
        except IndexError:
            continue
    return matched_routes

def fetch_live_data(route_name):
    """根據路線名稱取得即時到站資訊"""
    try:
        # 使用 taipei_route_info 抓取即時資料
        info = taipei_route_info(route_name, direction='go')  # 假設方向為 'go'
        df = info.parse_route_info()
        return df[['stop_name', 'arrival_info']]
    except Exception as e:
        print(f"❌ 無法取得路線 {route_name} 即時資料: {e}")
        return None

def main():
    """主程式入口"""
    start = input("請輸入出發站：").strip().lower()
    end = input("請輸入目的站：").strip().lower()

    # 1️⃣ 載入靜態資料
    df = load_static_data()

    # 2️⃣ 找出包含出發站與目的站的有效路線
    valid_routes = find_valid_routes(df, start, end)

    if not valid_routes:
        print("⚠️ 查無可搭乘路線，請確認站名是否正確。")
        return

    # 3️⃣ 爬取即時資料並輸出
    for route_name in valid_routes:
        print(f"\n🚌 路線：{route_name}")
        live_df = fetch_live_data(route_name)
        if live_df is not None:
            for _, row in live_df.iterrows():
                print(f"  🚏 {row['stop_name']} - 預估到站：{row['arrival_info']}")

if __name__ == "__main__":
    main()
