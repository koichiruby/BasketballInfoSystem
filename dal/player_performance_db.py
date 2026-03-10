from pymongo import MongoClient

class PlayerPerformanceDB:
    def __init__(self, db_url, db_name):
        # 连接 MongoDB 数据库
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['PlayerPerformances']

    def add_performance(self, performance_data):
        """
        插入新的球员比赛表现记录。
        :param performance_data: dict, 包含球员比赛表现的信息
        :return: 新添加文档的ID
        """
        return self.collection.insert_one(performance_data).inserted_id

    def find_performance(self, player_id, match_id):
        """
        根据 PlayerID 和 MatchID 查找球员比赛表现记录。
        :param player_id: str, 球员唯一标识
        :param match_id: str, 比赛唯一标识
        :return: 表现记录的字典数据，或 None 如果未找到
        """
        return self.collection.find_one({"PlayerID": player_id, "MatchID": match_id})

    def update_performance(self, player_id, match_id, update_data):
        """
        更新指定球员在指定比赛中的表现。
        :param player_id: str, 球员唯一标识
        :param match_id: str, 比赛唯一标识
        :param update_data: dict, 需要更新的数据
        :return: 更新操作的结果
        """
        return self.collection.update_one(
            {"PlayerID": player_id, "MatchID": match_id},
            {"$set": update_data}
        )

    def delete_performance(self, player_id, match_id):
        """
        删除指定球员在指定比赛中的表现记录。
        :param player_id: str, 球员唯一标识
        :param match_id: str, 比赛唯一标识
        :return: 删除操作的结果
        """
        return self.collection.delete_one({"PlayerID": player_id, "MatchID": match_id})

    def get_all_performances(self):
        """
        获取所有球员的比赛表现记录。
        :return: 包含所有表现记录的列表
        """
        return list(self.collection.find({}))
