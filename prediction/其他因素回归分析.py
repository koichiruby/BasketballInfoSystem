import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA

# 文件路径
file_path = r'C:\Users\kochi\Desktop\team.csv'

# 读取数据，确保使用正确的分隔符（逗号），并修正列名
df = pd.read_csv(file_path, sep=',')  # 使用正确的文件路径

# 清理列名：去除不必要的空格或字符
df.columns = df.columns.str.strip()
# 选择数值型列并填充缺失值
numeric_cols = df.select_dtypes(include=[np.number]).columns  # 选择所有数值型列
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())  # 用均值填补数值型列的缺失值


# 计算胜负比（WL）
'''if 'W' in df.columns and 'L' in df.columns:
    df['WL'] = df['W'] / (df['W'] + df['L'])
else:
    print("数据框中缺少 'W' 或 'L' 列，无法计算胜负比")'''

# 选择自变量（去除WL列和其他无关列如Team, Arena等）
X = df[['PTS','AST','STL','BLK','TOV','PF','TRB','FG%','3P%','2P%','FT%']]
y = df['W\L']

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用PCA降维来解决多重共线性问题
#pca = PCA(n_components=5)  # 假设我们减少到5个主成分
#X_pca = pca.fit_transform(X_scaled)
X_pca=X_scaled
# 在 X 数据中加入常数项（截距项）
X_pca = sm.add_constant(X_pca)

# 创建训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.3, random_state=42)

# 创建并拟合回归模型（使用 statsmodels）
model = sm.OLS(y_train, X_train)  # OLS：最小二乘法回归
results = model.fit()

# 打印回归结果摘要，包括t值、p值等
print(results.summary())

# 预测测试集
y_pred = results.predict(X_test)

# 计算均方误差（MSE）和 R² 值
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (MSE): {mse}')
print(f'R-squared: {r2}')

# 设置字体，解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')  # 添加对角线
plt.xlabel('真实值')
plt.ylabel('预测值')
plt.title('回归分析：真实值与预测值')
plt.show()

# 绘制残差图
residuals = y_test - y_pred
plt.scatter(y_pred, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('预测值')
plt.ylabel('残差')
plt.title('回归分析：预测值与残差')
plt.show()