import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 文件路径
file_path = r'C:\Users\kochi\Desktop\team.csv'

# 读取数据，确保使用正确的分隔符（逗号），并修正列名
df = pd.read_csv(file_path, sep=',')  # 使用正确的文件路径

# 清理列名：去除不必要的空格或字符
df.columns = df.columns.str.strip()

# 选择数值型列
numeric_cols = df.select_dtypes(include=[np.number]).columns  # 选择所有数值型列

# 设置字体，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用 SimHei 字体，支持中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 绘制箱线图
plt.figure(figsize=(10, 6))

# 针对每一列数据绘制箱线图
df[numeric_cols].boxplot(figsize=(12, 8))

# 设置标题
plt.title('Boxplot 检查异常值', fontsize=16)
plt.xticks(rotation=90)  # 如果列名较长，可以旋转x轴标签

# 显示图像
plt.show()
