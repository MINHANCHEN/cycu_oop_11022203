import sys
from datetime import datetime, timezone

# 強制設置編碼為 UTF-8（避免中文字顯示錯誤）
sys.stdout.reconfigure(encoding='utf-8')

# 中文星期對照表
WEEKDAY_MAP = {
    1: '星期一',
    2: '星期二',
    3: '星期三',
    4: '星期四',
    5: '星期五',
    6: '星期六',
    7: '星期日'
}

# Julian Day 計算公式
def to_julian_date(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    a = (14 - dt.month) // 12
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3
    jdn = dt.day + ((153 * m + 2) // 5) + 365 * y
    jdn += y // 4 - y // 100 + y // 400 - 32045
    jd = jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400
    return jd

def analyze_datetime(input_str):
    try:
        # 解析輸入的時間字串
        input_dt = datetime.strptime(input_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return "❌ 時間格式錯誤，請使用正確格式：YYYY-MM-DD HH:MM"

    # 當下時間（UTC）
    now_dt = datetime.now(timezone.utc)

    # Julian Dates
    input_jd = to_julian_date(input_dt)
    now_jd = to_julian_date(now_dt)

    # 計算經過的太陽日數
    days_passed = now_jd - input_jd

    # 中文星期幾
    weekday_str = WEEKDAY_MAP[input_dt.isoweekday()]

    # 當年的第幾天
    day_of_year = input_dt.timetuple().tm_yday

    # 回傳所有結果
    return {
        "weekday": weekday_str,
        "day_of_year": day_of_year,
        "julian_days_passed": round(days_passed, 6)
    }

if __name__ == "__main__":
    user_input = input("請輸入時間（格式為 YYYY-MM-DD HH:MM）：")
    result = analyze_datetime(user_input)

    if isinstance(result, str):
        print(result)  # 錯誤訊息
    else:
        print(f"📅 星期幾：{result['weekday']}")
        print(f"📆 當年的第 {result['day_of_year']} 天")
        print(f"🕒 從該時間到現在共經過了 {result['julian_days_passed']} 個太陽日（Julian Days）")
