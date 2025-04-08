import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

# 參數設定
mu = 1.5
sigma = 0.4
s = sigma
scale = np.exp(mu)

# 建立 x 軸範圍
x = np.linspace(0.01, 10, 1000)

# 計算 CDF
cdf = lognorm.cdf(x, s=s, scale=scale)

# 繪圖
plt.figure(figsize=(8, 5))
plt.plot(x, cdf, label='Lognormal CDF')
plt.title('Lognormal Cumulative Distribution Function')
plt.xlabel('x')
plt.ylabel('CDF')
plt.grid(True)
plt.legend()
plt.show()
