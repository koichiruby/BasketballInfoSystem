from pymongo import MongoClient

class TeamPerformanceDB:
    def __init__(self, db_url, db_name):
        # 连接 MongoDB 数据库
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['TeamPerformances']

    def add_team_performance(self, performance_data):
        """插入新的队伍表现信息"""
        return self.collection.insert_one(performance_data).inserted_id

    def find_team_performance(self, team_id, match_id):
        """根据 TeamID 和 MatchID 查找队伍表现信息"""
        return self.collection.find_one({"TeamID": team_id, "MatchID": match_id})

    def update_team_performance(self, team_id, match_id, update_data):
        """更新指定队伍的表现信息"""
        return self.collection.update_one({"TeamID": team_id, "MatchID": match_id}, {"$set": update_data})

    def delete_team_performance(self, team_id, match_id):
        """删除指定队伍的表现信息"""
        return self.collection.delete_one({"TeamID": team_id, "MatchID": match_id})
