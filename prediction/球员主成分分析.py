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

# 计算每个球员的主成分得分
pc_scores = pd.DataFrame(pca_result, columns=[f"PC{i+1}" for i in range(3)])

# 将球员名字和主成分得分结合
pc_scores['Player'] = data['Player']  # 假设球员名字在 'Player' 列中

# 获取队名
pc_scores['Tm'] = data['Tm']  # 假设队名在 'Tm' 列中

# 计算每个球员的综合得分
# 获取每个主成分的方差解释比例（即每个主成分的权重）
explained_variance_ratio = pca.explained_variance_ratio_

# 计算综合得分
pc_scores['Score'] = (pc_scores['PC1'] * explained_variance_ratio[0] +
                      pc_scores['PC2'] * explained_variance_ratio[1] +
                      pc_scores['PC3'] * explained_variance_ratio[2])

# 排名
pc_scores['Rank'] = pc_scores['Score'].rank(ascending=False)

# 按Rank升序排序
pc_scores_sorted = pc_scores.sort_values(by='Rank', ascending=True)

# 输出每个球员的得分和排名
print("每个球员的得分和排名:")
print(pc_scores_sorted[['Player', 'Tm', 'Score', 'Rank']])

# 如果需要，可以将结果保存为新的CSV文件
pc_scores_sorted.to_csv('player_scores_with_rank.csv', index=False)
