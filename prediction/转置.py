import numpy as np
import pandas as pd

# 原始数据
original_data = np.array([
    [0.27630099, 0.4310755, 0.06686198, 0.37415928, 0.17375438, 0.3604896,
     0.26325508, 0.08517362, 0.33742087, 0.13574026, 0.47369463],
    [-0.40351235, 0.10974132, -0.39989288, 0.03626941, 0.50628423, -0.23655823,
     0.02374373, 0.51854435, 0.01874898, 0.28275634, -0.04320469],
    [-0.3210573, -0.18123939, 0.3706821, -0.37281549, -0.0616919, 0.33479052,
     0.00695454, 0.14282197, 0.60210448, 0.24684759, -0.16696489]
])

# 转置数据
transposed_data = original_data.T

# 指标名称
features = ['MP', 'FG', '3P', 'FT', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

# 将转置后的数据转换为 DataFrame
index = [f"PC{i+1}" for i in range(original_data.shape[0])]
df = pd.DataFrame(original_data, index=index, columns=features)

# 输出结果
print("转置后的数据:")
print(df)

# 保存为 Excel 文件
df.to_excel('transposed_data.xlsx', index=True)
