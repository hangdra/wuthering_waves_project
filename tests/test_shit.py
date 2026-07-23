import numpy as np
def equal_probability_gaussian(a, b, sigma=0.15):
    """
    高斯核概率函数

    参数：
        sigma: 标准差，控制"多近算接近"

    P(equal) = exp(-(a-b)² / (2*sigma²))
    """
    diff_sq = (a - b) ** 2
    return np.exp(-diff_sq / (2 * sigma ** 2))

print(equal_probability_gaussian(0.4,0.0))
print(equal_probability_gaussian(0.3,0.0))