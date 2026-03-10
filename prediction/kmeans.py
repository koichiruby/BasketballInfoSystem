import pandas as pd

# 假设数据存储在名为 'nba_teams_stats.csv' 的文件中，使用逗号作为分隔符
data = pd.read_csv(r'D:\pycharmprojects\SPAN\merged_player_team_data.csv', sep=',')

# 查看数据的前几行，确保数据加载正确
print(data.head())

# 打印列名检查是否正确加载
print(data.columns)

# 使用列表推导式修正列名，去掉多余的空格和逗号
data.columns = [col.split(',')[0].strip() for col in data.columns]

# 再次检查列名是否已正确修正
print(data.columns)

# 选择需要进行聚类分析的核心球员的技术统计列
features = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'TOV', 'FG%', '3P%']  # 根据实际列名进行修改

# 确保列名正确后，再提取相关列
X = data[features]

# 数据标准化处理
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 进行层次聚类
from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=3)  # 假设选择3个聚类
data['Cluster'] = cluster.fit_predict(X_scaled)

# 输出聚类结果
print(data[['Player', 'Tm', 'Cluster']])

# 可视化聚类结果
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='PTS', y='AST', hue='Cluster', palette='viridis')
plt.title('Cluster of Teams Based on Core Players Stats')
plt.xlabel('Points per Game (PTS)')
plt.ylabel('Assists per Game (AST)')
plt.show()
# 计算聚类后每个聚类的核心球员得分均值与球队得分的相关性
#cluster_score_pts = data.groupby('Cluster')[['Score', 'PTS']].mean()
# 按 Cluster 分组计算 Score 和 PTS 的中位数
cluster_score_pts_median = data.groupby('Cluster')[['Score', 'PTS']].median()

# 打印结果
print(cluster_score_pts_median)

#print(cluster_score_pts)

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Score', y='PTS', data=data, hue='Cluster', palette='viridis')
plt.title('Relationship Between Core Player Score and Team Performance (PTS)')
plt.xlabel('Core Player Score (Score)')
plt.ylabel('Team Performance (PTS)')
plt.show()

# 保存聚类结果到新的CSV文件
data.to_csv('nba_teams_with_clusters.csv', index=False)
