from datetime import datetime, timezone

def calculate_julian_info(input_time_str: str):
    """
    輸入格式：'YYYY-MM-DD HH:MM'
    輸出：
        - 該日為星期幾（中文）
        - 輸入時間至今的太陽日差距（浮點數）
    """
    # 1. 將輸入字串轉為 datetime 物件
    try:
        input_dt = datetime.strptime(input_time_str, "%Y-%m-%d %H:%M")
        input_dt = input_dt.replace(tzinfo=timezone.utc)  # 將 input_dt 設為 UTC 時區
    except ValueError:
        print("❌ 時間格式錯誤，請使用 'YYYY-MM-DD HH:MM'")
        return

    # 2. 取得星期幾（中文）
    weekdays_zh = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = weekdays_zh[input_dt.weekday()]

    # 3. 計算該時間與現在時間的日數差（以浮點表示）
    now = datetime.now(timezone.utc)  # 使用時區感知的 UTC 時間
    time_delta = now - input_dt
    days_passed = time_delta.total_seconds() / 86400.0  # 1 太陽日 = 86400 秒

    # 4. 計算輸入時間的 Julian Date
    def to_julian_date(dt: datetime) -> float:
        # 轉換為 Julian Day Number（JD）
        a = (14 - dt.month) // 12
        y = dt.year + 4800 - a
        m = dt.month + 12 * a - 3
        jdn = dt.day + ((153 * m + 2) // 5) + 365 * y
        jdn += y // 4 - y // 100 + y // 400 - 32045
        # 加上當日時間的比例
        day_fraction = (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400
        return jdn + day_fraction

    julian_start = to_julian_date(input_dt)
    julian_now = to_julian_date(now)
    julian_diff = julian_now - julian_start

    # 5. 輸出結果（移除 emoji，避免編碼問題）
    print(f"該日是：{weekday_str}")
    print(f"該時刻的 Julian 日期為：{julian_start:.5f}")
    print(f"至今已過太陽日（Julian 日數）：{julian_diff:.5f}")

calculate_julian_info("2020-04-15 20:30")
