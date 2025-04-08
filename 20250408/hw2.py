import sys
from datetime import datetime, timezone

# 強制設置編碼為 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Julian Day 計算公式（修正）
def to_julian_date(dt):
    # 如果時間是本地時間，轉換為 UTC 時間
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)  # 轉換為 UTC

    # 儒略日（Julian Day）的計算公式
    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + ((153 * m + 2) // 5) + 365 * y
    jdn += y // 4 - y // 100 + y // 400 - 32045
    
    # 加上小時、分鐘、秒對應的小數部分
    jd = jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400
    return jd

def compute_julian_and_weekday(input_str):
    try:
        # 輸入時間格式：YYYY-MM-DD HH:MM
        input_dt = datetime.strptime(input_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return "❌ 時間格式錯誤，請使用正確格式：YYYY-MM-DD HH:MM"
    
    # 計算該時間的 Julian Day
    input_julian = to_julian_date(input_dt)
    
    # 回傳星期幾和經過的太陽日數（從公元前4713年1月1日12:00 UTC開始）
    weekday = input_dt.strftime("%A")  # 取得星期幾
    return weekday, round(input_julian, 6)

# 讓使用者輸入時間
user_input = input("請輸入時間（格式為 YYYY-MM-DD HH:MM）：")
weekday, jd = compute_julian_and_weekday(user_input)
print("星期幾：", weekday)
print("距離公元前4713年1月1日 12:00 UTC 所經過的太陽日數（Julian）：", jd)