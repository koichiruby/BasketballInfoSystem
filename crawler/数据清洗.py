import pandas as pd
import numpy as np
import re

# 1. 读取原始数据
df_raw = pd.read_csv(r"C:\Users\kochi\Desktop\atp_players_detailed.csv", encoding="utf-8")

# 2. 删除无用列
drop_cols = ["Follow player", "Profile Link", "Coach", "YTD - Move"]
df = df_raw.drop(columns=[col for col in drop_cols if col in df_raw.columns])

# 3. 百分比列转换为浮点数
percent_cols = [col for col in df.columns if df[col].astype(str).str.contains('%').any()]
for col in percent_cols:
    df[col] = df[col].astype(str).str.replace('%', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce') / 100

# 4. 数字列统一（去掉千位分隔符和$符号）
money_cols = ["YTD - Prize Money", "Career - Prize Money Singles & Doubles Combined"]
for col in money_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'[^0-9.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# 5. 胜率列拆分
if "YTD - W-L" in df.columns:
    df[["Wins", "Losses"]] = df["YTD - W-L"].str.extract(r"(\d+)\s*[-–]\s*(\d+)")
    df["Wins"] = pd.to_numeric(df["Wins"], errors='coerce')
    df["Losses"] = pd.to_numeric(df["Losses"], errors='coerce')
    df["Win Rate"] = df["Wins"] / (df["Wins"] + df["Losses"])
    df.drop(columns=["YTD - W-L"], inplace=True)

# 6. 身高处理 (格式如 "6'3\" (191cm)")
def convert_height(h):
    if pd.isna(h):
        return np.nan
    match = re.search(r'(\d+)\s*cm', h)
    return int(match.group(1)) if match else np.nan

df["Height_cm"] = df["Height"].apply(convert_height)

# 7. 体重处理 (格式如 "170 lbs (77kg)")
def convert_weight(w):
    if pd.isna(w):
        return np.nan
    match = re.search(r'(\d+)\s*kg', w)
    return int(match.group(1)) if match else np.nan

df["Weight_kg"] = df["Weight"].apply(convert_weight)

# 8. 年龄处理
def extract_age(age_str):
    if isinstance(age_str, str):
        match = re.match(r'(\d+)', age_str)
        return int(match.group(1)) if match else np.nan
    return age_str

df["Age"] = df["Age"].apply(extract_age)

# 9. 填充缺失值（数值列用均值）
for col in df.select_dtypes(include=['float64', 'int64']).columns:
    df[col] = df[col].fillna(df[col].mean())

# 10. 重命名列（可选，方便后续处理）
df.rename(columns={
    "Full Stats - Aces": "Aces",
    "Full Stats - Double Faults": "DoubleFaults",
    "Full Stats - Break Points Saved": "BreakPointsSaved",
    "Full Stats - Break Points Converted": "BreakPointsConverted",
    "Full Stats - 1st Serve": "FirstServeIn",
    "Full Stats - 1st Serve Points Won": "FirstServeWon",
    "Full Stats - 2nd Serve Points Won": "SecondServeWon",
    "Full Stats - 1st Serve Return Points Won": "FirstServeReturnWon",
    "Full Stats - 2nd Serve Return Points Won": "SecondServeReturnWon",
    "Full Stats - Return Points Won": "ReturnPointsWon",
    "Full Stats - Total Service Points Won": "TotalServicePointsWon",
    "Full Stats - Total Points Won": "TotalPointsWon",
}, inplace=True)

# 11. 保存清洗后的数据
df.to_csv("cleaned_atp_players.csv", index=False)
print("✅ 数据清洗完毕，已保存为 cleaned_atp_players.csv")
