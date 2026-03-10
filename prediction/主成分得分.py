import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 假设数据存储在名为 'core_players.csv' 的文件中，使用分号作为分隔符
data = pd.read_csv(r'D:\pycharmprojects\SPAN\core_players.csv', sep=';')

# 查看数据的前几行，确保数据加载正确
print(data.head())

# 选择需要进行PCA分析的特征列
features = ['MP', 'FG', '3P', 'FT', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

# 提取相关列
X = data[features]

# 数据标准化处理
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 进行PCA分析，假设我们提取前3个主成分
pca = PCA(n_components=3)
pca_result = pca.fit_transform(X_scaled)

# 输出主成分分析的结果
print("主成分分析结果:")
print(pca_result)

# 查看每个主成分的方差解释比例
print(f"每个主成分的方差解释比例: {pca.explained_variance_ratio_}")

# 将PCA结果添加到原始数据中，便于进一步分析
data['PCA1'] = pca_result[:, 0]
data['PCA2'] = pca_result[:, 1]
data['PCA3'] = pca_result[:, 2]

# 可视化PCA结果（用前两个主成分进行二维可视化）
plt.figure(figsize=(8, 6))
plt.scatter(data['PCA1'], data['PCA2'], c=data['PTS'], cmap='viridis', edgecolors='k')
plt.colorbar(label='Points (PTS)')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of NBA Player Stats')
plt.show()

# 如果需要，可以将结果保存为新的CSV文件
data.to_csv('player_stats_with_pca.csv', index=False)

# 输出主成分的载荷（即每个原始特征的贡献）
print("主成分的载荷：")
print(pca.components_)

# 输出每个主成分的特征重要性（即每个特征对主成分的影响）
feature_importance = pd.DataFrame(pca.components_, columns=features, index=[f"PC{i+1}" for i in range(3)])
print(feature_importance)

# 计算每个球员的主成分得分
pc_scores = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(3)])

# 将球员名字和主成分得分结合
pc_scores['Player'] = data['Player']  # 假设球员名字在 'Player' 列中

# 输出每个球员的主成分得分
print("每个球员的主成分得分:")
print(pc_scores[['Player', 'PC1', 'PC2', 'PC3']])
