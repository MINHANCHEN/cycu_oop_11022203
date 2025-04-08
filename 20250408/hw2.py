from datetime import datetime
from astropy.time import Time

import sys
sys.stdout.reconfigure(encoding='utf-8')
def time_info(input_time_str):
    # 解析輸入時間（格式為 YYYY-MM-DD HH:MM）
    input_dt = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
    
    # 取得星期幾
    weekday = input_dt.strftime('%A')  # e.g., 'Wednesday'
    
    # 使用 astropy 計算 Julian Date
    input_jd = Time(input_dt).jd
    now_jd = Time(datetime.utcnow()).jd  # 使用 UTC 為標準
    
    # 計算經過幾個太陽日
    days_passed = now_jd - input_jd

    print(f"輸入時間：{input_dt}")
    print(f"該天是星期：{weekday}")
    print(f"該時刻的 Julian Date：{input_jd:.5f}")
    print(f"目前 Julian Date：{now_jd:.5f}")
    print(f"至今經過的太陽日數：約 {days_passed:.5f} 天")
time_info("2025-04-08 18:30")
