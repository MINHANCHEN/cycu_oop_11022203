import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV data
df = pd.read_csv('20250520/midterm_scores.csv')

# 科目列表
subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']

# 設定分數範圍 (0-10, 10-20, ..., 90-100)
bins = np.arange(0, 110, 10)
bin_centers = (bins[:-1] + bins[1:]) / 2  # 計算每個分數範圍的中心點

# 設定顏色
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink']

# 初始化圖表
plt.figure(figsize=(12, 8))

# 計算每個科目的分數分佈並繪製
width = 1 / (len(subjects) + 1)  # 每個條形的寬度
for i, (subj, color) in enumerate(zip(subjects, colors)):
    counts, _ = np.histogram(df[subj], bins=bins)  # 計算每個分數範圍內的人數
    plt.bar(bin_centers + i * width, counts, width=width, color=color, label=subj, edgecolor='black')

# 設定圖表標題和軸標籤
plt.title('Distribution of Scores by Subject', fontsize=16)
plt.xlabel('Score Ranges', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.xticks(bin_centers + width * (len(subjects) - 1) / 2, [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins) - 1)])
plt.legend(title='Subjects')  # 顯示圖例

# 顯示圖表
plt.tight_layout()
plt.show()