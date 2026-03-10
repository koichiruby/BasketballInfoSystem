from pymongo import MongoClient

class MatchInfoDB:
    def __init__(self, db_url, db_name):
        # 连接 MongoDB 数据库
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['MatchInfo']  # 使用 Collection 来执行查询和插入

    def get_all_matches(self):
        """ 获取所有赛事数据 """
        return list(self.collection.find({}))

    def add_match_info(self, match_data):
        """
        添加新的比赛信息。
        :param match_data: dict, 包含比赛的详细信息
        :return: 新添加文档的ID
        """
        # 验证必要字段
        required_fields = ["MatchID", "MatchTime", "Location", "Teams", "Result", "Highlights", "KeyEvents"]
        for field in required_fields:
            if field not in match_data:
                raise ValueError(f"缺少必要字段：{field}")

        # 检查是否已存在相同 MatchID 的记录
        existing = self.find_match_info(match_data["MatchID"])
        if existing:
            raise ValueError("该场比赛记录已存在")

        # 插入新记录
        return self.collection.insert_one(match_data).inserted_id  # 使用 collection.insert_one

    def get_match_by_id(self, match_id):
        """
        根据 MatchID 获取赛事信息
        :param match_id: str，赛事的 MatchID
        :return: dict，赛事信息，如果未找到则返回 None
        """
        match = self.collection.find_one({"MatchID": match_id})
        return match

    def update_match_info(self, match_id, update_data):
        """更新指定比赛的信息"""
        return self.collection.update_one({"MatchID": match_id}, {"$set": update_data})

    def delete_match_info(self, match_id):
        """删除指定比赛的信息"""
        return self.collection.delete_one({"MatchID": match_id})

    def find_match_info(self, match_id):
        """根据 MatchID 查找是否已经存在该赛事记录"""
        # 使用 MongoDB 的 find_one() 方法查找
        return self.collection.find_one({"MatchID": match_id})  # 使用 collection.find_one() 来查找
