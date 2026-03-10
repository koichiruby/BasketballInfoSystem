from pymongo import MongoClient
#待实现，选择是通过数据库查询匹配登录还是通过config导入
class AuthDB:
    def __init__(self, db_url, db_name):
        # 连接 MongoDB 数据库
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['AuthInfo']

    def add_auth_info(self, auth_data):
        """
        添加新的认证信息。
        :param auth_data: dict, 包含认证信息的字典
        :return: 新添加文档的ID
        """
        return self.collection.insert_one(auth_data).inserted_id

    def find_auth_info(self, auth_id):
        """
        根据 AuthID 查找认证信息。
        :param auth_id: str, 用户或管理员的唯一标识
        :return: 认证信息的字典数据，或 None 如果未找到
        """
        return self.collection.find_one({"AuthID": auth_id})

    def authenticate(self, auth_id, keyword):
        """
        验证用户身份。
        :param auth_id: str, 用户或管理员的唯一标识
        :param keyword: str, 密码或关键字
        :return: True 如果认证成功，否则 False
        """
        auth_info = self.find_auth_info(auth_id)
        if auth_info and auth_info.get("keyword") == keyword:
            return True
        return False
