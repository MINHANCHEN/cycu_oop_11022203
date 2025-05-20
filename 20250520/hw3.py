import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import os

# 設定資料夾路徑
shp_dir = "20250520/taipei_town2"  # 地圖資料夾
bus_stops_file = "20250520/bus_stops.csv"  # 公車站牌資料
output_dir = "20250520/output"  # 輸出資料夾
os.makedirs(output_dir, exist_ok=True)

# 找出 taipei_town2 資料夾內的第一個 .shp 檔案
shp_file = None
for fname in os.listdir(shp_dir):
    if fname.endswith(".shp"):
        shp_file = os.path.join(shp_dir, fname)
        break

if shp_file is None:
    print("無法找到 .shp 檔案")
else:
    # 讀取地圖資料
    gdf = gpd.read_file(shp_file)

    # 檢查欄位名稱
    print("可用欄位:", gdf.columns)

    # 篩選北北基桃地區
    target_column = 'COUNTYNAME'  # 假設地區名稱欄位為 COUNTYNAME
    target_cities = ['台北市', '新北市', '基隆市', '桃園市']
    if target_column not in gdf.columns:
        raise KeyError(f"欄位 '{target_column}' 不存在，請檢查 .shp 檔案的欄位名稱")
    gdf_filtered = gdf[gdf[target_column].isin(target_cities)]

    # 匯出篩選後的地圖資料為 GeoJSON
    north_taiwan_geojson = os.path.join(output_dir, "north_taiwan_filtered.geojson")
    gdf_filtered.to_file(north_taiwan_geojson, driver="GeoJSON")
    print(f"北北基桃地圖已匯出至 {north_taiwan_geojson}")

    # 初始化變數
    bus_stops_gdf = None
    bus_route_gdf = None

    # 讀取公車站牌資料
    if os.path.exists(bus_stops_file):
        bus_stops = pd.read_csv(bus_stops_file)
        bus_stops_gdf = gpd.GeoDataFrame(
            bus_stops,
            geometry=gpd.points_from_xy(bus_stops['longitude'], bus_stops['latitude']),
            crs="EPSG:4326"
        )
        # 匯出公車站牌資料為 GeoJSON
        bus_stops_geojson = os.path.join(output_dir, "bus_stops.geojson")
        bus_stops_gdf.to_file(bus_stops_geojson, driver="GeoJSON")
        print(f"公車站牌資料已匯出至 {bus_stops_geojson}")
    else:
        print("無法找到公車站牌資料")

    # 建立公車路線資料
    if bus_stops_gdf is not None:
        # 將公車站點連接成線
        route_line = LineString(bus_stops_gdf.geometry.tolist())
        bus_route_gdf = gpd.GeoDataFrame(
            {'route_name': ['Bus Route'], 'geometry': [route_line]},
            crs="EPSG:4326"
        )
        # 匯出公車路線資料為 GeoJSON
        bus_route_geojson = os.path.join(output_dir, "bus_route.geojson")
        bus_route_gdf.to_file(bus_route_geojson, driver="GeoJSON")
        print(f"公車路線資料已匯出至 {bus_route_geojson}")
    else:
        print("無法建立公車路線資料")

    # 繪製地圖
    ax = gdf_filtered.plot(edgecolor='black', figsize=(10, 10), alpha=0.5, color='lightgrey')
    plt.title("北北基桃地圖與公車站牌及路線", fontsize=16)

    # 疊加公車站牌
    if bus_stops_gdf is not None:
        bus_stops_gdf.plot(ax=ax, color='red', markersize=10, label='公車站牌')

    # 疊加公車路線
    if bus_route_gdf is not None:
        bus_route_gdf.plot(ax=ax, color='blue', linewidth=2, label='公車路線')

    # 顯示圖例和調整比例
    plt.legend()
    plt.axis('equal')
    plt.show()