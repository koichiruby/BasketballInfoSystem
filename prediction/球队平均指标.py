import pandas as pd

# 1. 读取数据
file_path = r'C:\Users\kochi\Desktop\Regular.csv' # 替换为你的文件路径
data = pd.read_csv(file_path, sep=';', encoding='ISO-8859-1')  # 根据实际编码调整

# 2. 选择需要的指标
selected_columns = ['Tm', 'PTS', 'TRB', 'STL', 'BLK', 'AST', 'FG%', '3P%', 'FT%', 'TOV', 'PF']
data = data[selected_columns]

# 3. 数据清洗：处理缺失值（可选）
data = data.dropna()

# 4. 按球队分组，计算平均值
team_avg_stats = data.groupby('Tm').mean()

# 5. 输出结果
print("各球队的平均统计指标：")
print(team_avg_stats)

# 6. 保存结果到新文件（可选）
team_avg_stats.to_csv('team_average_stats.csv')
