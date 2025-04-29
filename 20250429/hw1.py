# -*- coding: utf-8 -*-  
import sys  
import io  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os  
import re  
import pandas as pd  
from playwright.sync_api import sync_playwright  
from sqlalchemy import create_engine, Column, String, Float, Integer  
from sqlalchemy.orm import sessionmaker, declarative_base  
import matplotlib.pyplot as plt  
from mpl_toolkits.basemap import Basemap  
from matplotlib.offsetbox import OffsetImage, AnnotationBbox  
from PIL import Image  

class taipei_route_list:  
    def __init__(self, working_directory='data'):  
        self.working_directory = working_directory  
        os.makedirs(self.working_directory, exist_ok=True)  
        self.url = 'https://ebus.gov.taipei/ebus?ct=all'  
        self.content = None  
        self._fetch_content()  

        Base = declarative_base()  

        class bus_route_orm(Base):  
            __tablename__ = 'data_route_list'  
            route_id = Column(String, primary_key=True)  
            route_name = Column(String)  
            route_data_updated = Column(Integer, default=0)  

        self.orm = bus_route_orm  
        self.engine = create_engine(f'sqlite:///{self.working_directory}/hermes_ebus_taipei.sqlite3')  
        self.engine.connect()  
        Base.metadata.create_all(self.engine)  
        Session = sessionmaker(bind=self.engine)  
        self.session = Session()  

    def _fetch_content(self):  
        with sync_playwright() as p:  
            browser = p.chromium.launch(headless=True)  
            page = browser.new_page()  
            page.goto(self.url)  
            page.wait_for_timeout(3000)  
            self.content = page.content()  
            browser.close()  
        with open(f'{self.working_directory}/hermes_ebus_taipei_route_list.html', "w", encoding="utf-8") as file:  
            file.write(self.content)  

    def parse_route_list(self) -> pd.DataFrame:  
        pattern = r'<li><a href="javascript:go\(\'(.*?)\'\)">(.*?)</a></li>'  
        matches = re.findall(pattern, self.content, re.DOTALL)  
        if not matches:  
            raise ValueError("No data found for route table")  
        bus_routes = [(route_id, route_name.strip()) for route_id, route_name in matches]  
        self.dataframe = pd.DataFrame(bus_routes, columns=["route_id", "route_name"])  
        return self.dataframe  

    def save_to_database(self):  
        for _, row in self.dataframe.iterrows():  
            self.session.merge(self.orm(route_id=row['route_id'], route_name=row['route_name']))  
        self.session.commit()  

    def read_from_database(self) -> pd.DataFrame:  
        query = self.session.query(self.orm)  
        self.db_dataframe = pd.read_sql(query.statement, self.session.bind)  
        return self.db_dataframe  

    def set_route_data_updated(self, route_id: str, route_data_updated: int = 1):  
        self.session.query(self.orm).filter_by(route_id=route_id).update({"route_data_updated": route_data_updated})  
        self.session.commit()  

    def set_route_data_unexcepted(self, route_id: str):  
        self.session.query(self.orm).filter_by(route_id=route_id).update({"route_data_updated": 2})  
        self.session.commit()  

    def __del__(self):  
        self.session.close()  
        self.engine.dispose()  


class taipei_route_info:  
    def __init__(self, route_id: str, direction: str = 'go', working_directory: str = 'data'):  
        self.route_id = route_id  
        self.direction = direction  
        self.working_directory = working_directory  
        os.makedirs(self.working_directory, exist_ok=True)  
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}'  
        if self.direction not in ['go', 'come']:  
            raise ValueError("Direction must be 'go' or 'come'")  
        self._fetch_content()  

    def _fetch_content(self):  
        with sync_playwright() as p:  
            browser = p.chromium.launch(headless=True)  
            page = browser.new_page()  
            page.goto(self.url)  
            if self.direction == 'come':  
                page.click('a.stationlist-come-go-gray.stationlist-come')  
            page.wait_for_timeout(3000)  
            self.content = page.content()  
            browser.close()  

    def parse_route_info(self) -> pd.DataFrame:  
        pattern = re.compile(  
            r'<li>.*?<span class="auto-list-stationlist-position.*?">(.*?)</span>\s*'  
            r'<span class="auto-list-stationlist-number">\s*(\d+)</span>\s*'  
            r'<span class="auto-list-stationlist-place">(.*?)</span>.*?'  
            r'<input[^>]+name="item\.UniStopId"[^>]+value="(\d+)"[^>]*>.*?'  
            r'<input[^>]+name="item\.Latitude"[^>]+value="([\d\.]+)"[^>]*>.*?'  
            r'<input[^>]+name="item\.Longitude"[^>]+value="([\d\.]+)"[^>]*>',  
            re.DOTALL  
        )  
        matches = pattern.findall(self.content)  
        if not matches:  
            raise ValueError(f"No data found for route ID {self.route_id}")  

        self.dataframe = pd.DataFrame(  
            matches,  
            columns=["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"]  
        )  
        self.dataframe["direction"] = self.direction  
        self.dataframe["route_id"] = self.route_id  
        return self.dataframe  

    def save_to_database(self):  
        db_file = f"{self.working_directory}/hermes_ebus_taipei.sqlite3"  
        engine = create_engine(f"sqlite:///{db_file}")  
        Base = declarative_base()  

        class bus_stop_orm(Base):  
            __tablename__ = "data_route_info_busstop"  
            stop_id = Column(Integer)  
            arrival_info = Column(String)  
            stop_number = Column(Integer, primary_key=True)  
            stop_name = Column(String)  
            latitude = Column(Float)  
            longitude = Column(Float)  
            direction = Column(String, primary_key=True)  
            route_id = Column(String, primary_key=True)  

        Base.metadata.create_all(engine)  
        Session = sessionmaker(bind=engine)  
        session = Session()  

        for _, row in self.dataframe.iterrows():  
            session.merge(bus_stop_orm(  
                stop_id=row["stop_id"],  
                arrival_info=row["arrival_info"],  
                stop_number=row["stop_number"],  
                stop_name=row["stop_name"],  
                latitude=row["latitude"],  
                longitude=row["longitude"],  
                direction=row["direction"],  
                route_id=row["route_id"]  
            ))  

        session.commit()  
        session.close()  

    def plot_route_map(self, output_path: str, highlight_stop_number: int = None):  
        df = self.dataframe.copy()  
        latitudes = df["latitude"].astype(float)  
        longitudes = df["longitude"].astype(float)  

        fig = plt.figure(figsize=(10, 8))  
        m = Basemap(projection='merc',  
                    llcrnrlat=min(latitudes) - 0.01,  
                    urcrnrlat=max(latitudes) + 0.01,  
                    llcrnrlon=min(longitudes) - 0.01,  
                    urcrnrlon=max(longitudes) + 0.01,  
                    resolution='i')  

        m.drawmapboundary(fill_color='lightblue')  
        m.fillcontinents(color='lightgray', lake_color='lightblue')  
        m.drawcoastlines()  
        m.drawrivers()  

        x, y = m(longitudes.values, latitudes.values)  
        m.plot(x, y, marker='o', color='red', linewidth=2)  

        for xi, yi, name in zip(x, y, df['stop_name']):  
            plt.text(xi, yi, name, fontsize=9, ha='left', va='bottom')  

        # 插入圖片在指定站序  
        if highlight_stop_number is not None:  
            row = df[df["stop_number"].astype(int) == highlight_stop_number]  
            if not row.empty:  
                xi, yi = m(float(row["longitude"].values[0]), float(row["latitude"].values[0]))  
                image_path = r"C:\Users\User\Documents\GitHub\cycu_oop_11022203\人.jpg"  # 更新路徑  
                if os.path.exists(image_path):  
                    img = Image.open(image_path)  
                    img = img.convert('RGB')  # 確保轉換為RGB模式（去除透明通道）  
                    img = img.resize((40, 40))  # 調整圖片大小  
                    imagebox = OffsetImage(img, zoom=1)  
                    ab = AnnotationBbox(imagebox, (xi, yi), frameon=False)  
                    plt.gca().add_artist(ab)  

        plt.title(f"Route Map: {self.route_id} ({self.direction})", fontsize=15)  
        plt.savefig(output_path, dpi=300)  
        plt.close()  


if __name__ == "__main__":  
    route_list = taipei_route_list()  
    route_list.parse_route_list()  
    route_list.save_to_database()  

    bus1 = '0161000900'  # 承德幹線  
    bus_list = [bus1]  

    for route_id in bus_list:  
        try:  
            route_info = taipei_route_info(route_id, direction="go")  
            route_info.parse_route_info()  
            route_info.save_to_database()  

            for index, row in route_info.dataframe.iterrows():  
                print(f"站序: {row['stop_number']}, 名稱: {row['stop_name']}, 緯度: {row['latitude']}, 經度: {row['longitude']}")  

            map_path = f"data/route_{route_id}_go.png"  
            route_info.plot_route_map(map_path, highlight_stop_number=5)  
            print(f"✅ 路線圖已儲存：{map_path}")  

            route_list.set_route_data_updated(route_id)  

        except Exception as e:  
            print(f"❌ 處理路線 {route_id} 發生錯誤: {e}")  
            route_list.set_route_data_unexcepted(route_id)
