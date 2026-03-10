from flask import session
from config import USERNAME, PASSWORD  # 导入配置

class AuthManager:
    @staticmethod
    def login(username, password):
        print(f"Trying to log in with username: {username} and password: {password}")  # 调试输出
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return True
        print("Login failed: username or password mismatch")  # 调试输出
        return False

    @staticmethod
    def is_logged_in():
        # 检查 'logged_in' 键是否存在于 session 中，并且其值为 True
        logged_in = session.get('logged_in', False)
        print(f"Checking if logged in: {logged_in}")  # 调试输出
        return logged_in

    @staticmethod
    def logout():
        # 退出登录时从 session 中删除 'logged_in' 键
        session.pop('logged_in', None)
        print("Logged out successfully")  # 调试输出

