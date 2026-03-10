# 🏀 Basketball Information System

A basketball data analysis and management platform that integrates **data crawling, data analysis, and web-based information management**.

The project collects basketball-related data through web crawling, performs statistical analysis and machine learning processing, and finally visualizes and manages the results through a **Flask-based web system**.

---

# 📌 Project Overview

This project integrates three major components:

1. **Data Crawling Module**
2. **Data Analysis & Prediction Module**
3. **Basketball Information Management System**

The system forms a complete data pipeline:

```
Data Crawling → Data Cleaning → Data Analysis → Prediction → Web Visualization
```

---

# 🏗 System Architecture

```
                ┌─────────────────┐
                │   Web Crawler   │
                │  (crawler)      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   Data Cleaning │
                │   & Processing  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Data Analysis & │
                │   Prediction    │
                │  (prediction)   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Flask Backend  │
                │ Basketball Info │
                │     System      │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Web Interface  │
                │ templates/static│
                └─────────────────┘
```

---

# 📂 Project Structure

```
BasketballInfoSystem
│
├── app.py                     # Flask application entry
├── config.py                  # System configuration
├── requirements.txt           # Python dependencies
├── README.md
│
├── bbl/                       # Business logic layer
│
├── dal/                       # Data access layer
│
├── crawler/                   # Web crawling module
│   ├── detailget.py           # Player detail crawler
│   ├── linkget.py             # Link crawler
│   ├── 数据清洗.py             # Data cleaning script
│   ├── 胜率预测.py             # Win probability analysis
│   ├── atp_players_page1.csv
│   ├── cleaned_atp_players.csv
│
├── prediction/                # Data analysis & prediction
│   ├── kmeans.py              # Player clustering
│   ├── nbcsv.py               # CSV processing
│   ├── 主成分得分.py            # PCA analysis
│   ├── 球员主成分分析.py
│   ├── 球队平均指标.py
│   ├── 核心球员.py
│   ├── 异常检测.py
│   ├── 相关性系数检验.py
│   ├── 整合.py
│   ├── 转置.py
│   ├── nba_teams_2024.csv
│   ├── player_stats_with_pca.csv
│
├── templates/                 # HTML templates
│
├── static/                    # Static resources (CSS/JS)
│
└── .gitignore
```

---

# 🚀 Features

### 1️⃣ Data Crawling

The crawler module collects basketball-related data from online sources.

Main tasks include:

* Player information crawling
* Link collection
* Page data extraction
* Data cleaning and preprocessing

---

### 2️⃣ Data Analysis

The prediction module performs statistical analysis on player and team data:

* **Principal Component Analysis (PCA)**
* **K-Means Clustering**
* **Correlation Analysis**
* **Outlier Detection**
* **Player Scoring Models**

These methods are used to analyze player performance and team statistics.

---

### 3️⃣ Win Probability Analysis

The project includes scripts for analyzing factors influencing **game winning probability**, helping evaluate team strength and player contributions.

---

### 4️⃣ Basketball Information System

The Flask backend provides a web-based system that supports:

* Player information management
* Team statistics management
* Match data display
* Data visualization

---

# 🛠 Technologies Used

| Category         | Technology               |
| ---------------- | ------------------------ |
| Backend          | Flask                    |
| Data Processing  | Pandas                   |
| Machine Learning | Scikit-learn             |
| Data Analysis    | NumPy                    |
| Visualization    | HTML / CSS               |
| Web Crawling     | Requests / BeautifulSoup |

---

# 📦 Installation

Clone the repository:

```bash
git clone https://github.com/koichiruby/BasketballInfoSystem.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the web application:

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# 📊 Data Analysis Pipeline

```
Web Crawling
      │
      ▼
Data Cleaning
      │
      ▼
Statistical Analysis
      │
      ▼
Machine Learning (PCA / Clustering)
      │
      ▼
Prediction & Evaluation
      │
      ▼
Web System Visualization
```

---

# 📚 Learning Objectives

This project demonstrates:

* Web crawling and data collection
* Data cleaning and preprocessing
* Statistical analysis techniques
* Machine learning applications in sports analytics
* Flask-based web application development

---

# 📄 License

This project is for **educational and research purposes**.
