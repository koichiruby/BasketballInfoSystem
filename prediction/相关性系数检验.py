import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr, spearmanr

# 数据
cluster_data = {
    'Cluster': [0, 1, 2],
    'Score': [-0.11819, -0.57269, 0.91435],
    'PTS': [7.488636, 8.888889, 8.363864]
}

# 创建 DataFrame
df = pd.DataFrame(cluster_data)

# 创建 Z-score 标准化器
scaler = StandardScaler()

# 对 Score 和 PTS 列进行标准化
df[['Score', 'PTS']] = scaler.fit_transform(df[['Score', 'PTS']])

# 计算皮尔逊相关系数和 p 值
pearson_corr, pearson_p_value = pearsonr(df['Score'], df['PTS'])

# 计算Spearman秩相关系数和 p 值
spearman_corr, spearman_p_value = spearmanr(df['Score'], df['PTS'])

# 输出结果
print(f"皮尔逊相关系数: {pearson_corr}")
print(f"皮尔逊 p 值: {pearson_p_value}")
print(f"Spearman 秩相关系数: {spearman_corr}")
print(f"Spearman p 值: {spearman_p_value}")
