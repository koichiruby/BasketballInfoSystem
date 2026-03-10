import pandas as pd

# 1. 读取数据
file_path = r'C:\Users\kochi\Desktop\Regular.csv'  # 替换为你的文件路径
data = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1')
# 2. 选择需要的指标
selected_columns = ['Tm', 'Player', 'PTS', 'TRB', 'STL', 'BLK', 'AST', 'FG%', '3P%', 'FT%', 'TOV', 'PF']
data = data[selected_columns]

# 3. 将数值列和非数值列分开
numeric_columns = ['PTS', 'TRB', 'STL', 'BLK', 'AST', 'FG%', '3P%', 'FT%', 'TOV', 'PF']
team_avg_stats = data.groupby('Tm')[numeric_columns].mean().reset_index()

# 4. 筛选核心球员（每队得分最高的球员，仅保留得分）
core_players = data.loc[data.groupby('Tm')['PTS'].idxmax(), ['Tm', 'Player', 'PTS']].reset_index(drop=True)

# 5. 合并核心球员数据与球队平均表现
result = pd.merge(core_players, team_avg_stats, on='Tm', how='left')

# 6. 输出结果
print("核心球员得分与球队平均表现合并后的数据：")
print(result)

# 7. 保存结果到新文件（可选）
result.to_csv('core_players_with_team_avg.csv', index=False)
