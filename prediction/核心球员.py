import pandas as pd

# 文件路径
file_path = r'C:\Users\kochi\Desktop\Regular.csv'
data = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1')
# 检查列名
print(data.columns)

# 去除列名中的空格
data.columns = data.columns.str.strip()

# 如果需要，调整列名
# data = data.rename(columns={'player': 'Player'})  # 根据需要调整列名

# 保留你需要的列
columns_to_keep = ['Player', 'Tm', 'PTS', 'TRB', 'STL', 'BLK', 'AST', 'FG%', '3P%', 'FT%', 'TOV', 'PF']
data = data[columns_to_keep]

# 按照'Player'和'Tm'分组并计算均值
data = data.groupby(['Player', 'Tm'], as_index=False).mean()


# 4. 计算核心评分
# 定义权重
weights = {'PTS': 0.4, 'TRB': 0.3, 'AST': 0.2, 'TOV': -0.1}

# 添加一个新的列：核心评分
data['core_score'] = (data['PTS'] * weights['PTS'] +
                     data['TRB'] * weights['TRB'] +
                     data['AST'] * weights['AST'] +
                     data['TOV'] * weights['TOV'])

# 5. 按球队选出核心球员
core_players = data.loc[data.groupby('Tm')['core_score'].idxmax()]

# 6. 输出结果
print("每支球队的核心球员：")
print(core_players[['Tm', 'Player', 'core_score']])
