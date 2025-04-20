import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_pdf(mu, sigma, filename='normal_pdf.jpg'):
    # 建立 x 軸範圍（以平均值為中心，左右各延伸 4 個標準差）
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)

    # 計算 PDF
    pdf = norm.pdf(x, loc=mu, scale=sigma)

    # 繪圖
    plt.figure(figsize=(8, 5))
    plt.plot(x, pdf, label=f'Normal PDF\nmu={mu}, sigma={sigma}')
    plt.title('Normal Distribution - Probability Density Function')
    plt.xlabel('x')
    plt.ylabel('PDF')
    plt.grid(True)
    plt.legend()

    # 儲存圖檔
    plt.savefig(filename)
    print(f"圖形已儲存為 {filename}")
    plt.show()

if __name__ == "__main__":
    try:
        # 從終端機讀取 mu 與 sigma
        mu = float(input("請輸入 mu（平均值）: "))
        sigma = float(input("請輸入 sigma（標準差）: "))

        # 檢查 sigma 是否為正數
        if sigma <= 0:
            raise ValueError("sigma 必須大於 0")

        # 呼叫繪圖函數
        plot_normal_pdf(mu, sigma)

    except ValueError as e:
        print(f"輸入錯誤：{e}")
