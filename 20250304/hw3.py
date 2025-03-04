import math

# 修正後的絕對值函式
def absolute_value(x):
    if x < 0:
        return -x
    return x  # 直接返回 x，處理 x == 0 和 x > 0

# 更簡潔的整除判斷函式
def is_divisible(x, y):
    return x % y == 0  # 直接返回布林值

# 計算兩點距離的函式
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# 測試函式
if __name__ == "__main__":
    # 測試 absolute_value
    print(f"absolute_value(-5): {absolute_value(-5)}")  # 應輸出 5
    print(f"absolute_value(0): {absolute_value(0)}")    # 應輸出 0
    print(f"absolute_value(8): {absolute_value(8)}")    # 應輸出 8

    # 測試 is_divisible
    print(f"is_divisible(10, 2): {is_divisible(10, 2)}")  # 應輸出 True
    print(f"is_divisible(10, 3): {is_divisible(10, 3)}")  # 應輸出 False

    # 測試 distance
    print(f"distance(0, 0, 3, 4): {distance(0, 0, 3, 4)}")  # 應輸出 5.0 (3-4-5 三角形)
    print(f"distance(1, 2, 4, 6): {distance(1, 2, 4, 6)}")  # 應輸出 5.0