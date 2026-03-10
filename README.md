# 🏀 Basketball Information System

A web-based basketball information management system built with **Flask**.
The system supports player information management, team management, match data management, and performance statistics.

This project demonstrates a **modular Flask backend architecture** for sports data management.

---

# 📌 Features

* Player Information Management
* Team Information Management
* Match Data Management
* Player Performance Statistics
* Team Performance Analysis
* User Authentication System

---

# 🏗 System Architecture

The project follows a **modular Flask architecture**, separating business logic from the main application.

```
Client (Browser)
        │
        ▼
Flask Web Server (app.py)
        │
        ▼
Business Logic Layer (bbl modules)
        │
        ▼
Database / Data Storage
```

Main components:

| Module       | Description            |
| ------------ | ---------------------- |
| `app.py`     | Main Flask application |
| `config.py`  | System configuration   |
| `bbl/`       | Business logic modules |
| `templates/` | HTML templates         |
| `static/`    | Static resources       |

---

# 📂 Project Structure

```
BasketballInfoSystem
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── bbl/
│   ├── auth_manager.py
│   ├── playerinfo_manager.py
│   ├── matchinfo_manager.py
│   ├── playerperformance_manager.py
│   ├── teaminfo_manager.py
│   └── teamperformance_manager.py
│
├── templates/
│
└── static/
```

---

# 🚀 Installation

Clone the repository:

```
git clone https://github.com/YOURNAME/BasketballInfoSystem.git
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the project:

```
python app.py
```

Then open in browser:

```
http://127.0.0.1:5000
```

---

# 🖼 System Screenshots

### Player Information Management

![player](docs/player.png)

### Team Management

![team](docs/team.png)

### Match Data

![match](docs/match.png)

---

# 🧠 Technologies Used

* Python
* Flask
* Pandas
* SQLAlchemy / PyMySQL
* HTML / CSS
* Jinja2 Templates

---

# 📚 Learning Purpose

This project is developed for learning purposes, focusing on:

* Web backend development
* Modular project structure
* Sports data management systems

---

# 📄 License

This project is released for educational use.
## System Architecture

```mermaid
graph TD

A[Browser Client] --> B[Flask App]
B --> C[Auth Manager]
B --> D[Player Manager]
B --> E[Team Manager]
B --> F[Match Manager]
B --> G[Performance Manager]

C --> H[Database]
D --> H
E --> H
F --> H
G --> H