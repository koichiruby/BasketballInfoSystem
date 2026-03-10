import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt  # 新增导入

# 1. 读取数据
df = pd.read_csv('cleaned_atp_players.csv')

# 2. 剔除无关及泄露变量
drop_cols = [
    'Name', 'Unnamed: 1', 'Birthplace', 'Country', 'Plays',
    'Wins', 'Losses', 'Win Rate', 'WinRate', 'Career - W-L',
    'Height', 'Weight', 'Height_cm', 'Weight_kg',
    'Career - Prize Money Singles & Doubles Combined','YTD - Rank', 'YTD - Prize Money'
]
cols_to_drop = [col for col in drop_cols if col in df.columns]
df_model = df.drop(columns=cols_to_drop)

# 3. 将数据转换为数值类型，无法转换的设为NaN
df_model = df_model.apply(pd.to_numeric, errors='coerce')

# 4. 目标变量
target_col = 'Win Rate' if 'Win Rate' in df.columns else 'WinRate'
y = df[target_col]

# 5. 处理缺失值：用均值填充
X = df_model.fillna(df_model.mean())

# 6. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 7. 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 8. 建立随机森林回归模型
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 9. 预测与评估
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse:.4f}')
print(f'R2 Score: {r2:.4f}')

# 10. 特征重要性
feat_importance = pd.Series(model.feature_importances_, index=X.columns)
feat_importance = feat_importance.sort_values(ascending=False)
print('Top 10 important features:')
print(feat_importance.head(10))

# 11. 可视化特征重要性
top_features = feat_importance.head(10)
plt.figure(figsize=(10,6))
top_features.plot(kind='bar')
plt.title('Top 10 Important Features')
plt.ylabel('Feature Importance')
plt.xlabel('Features')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
