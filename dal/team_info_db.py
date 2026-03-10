from pymongo import MongoClient

class TeamDB:
    def __init__(self, db_url, db_name):
        # 连接 MongoDB 数据库
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['TeamInfo']


    def get_all_teams(self):
        """获取所有球队"""
        return list(self.collection.find())  # 返回所有文档
    def get_team_by_id(self, team_id):
        """
        根据 TeamID 查找团队
        :param team_id: 团队的唯一标识符
        :return: 返回团队数据或 None
        """
        return self.collection.find_one({"TeamID": team_id})  # 查询 TeamID 匹配的团队

    def add_team(self, team_data):
        """插入新的队伍信息"""
        #return self.collection.insert_one(team_data).inserted_id
        result = self.collection.insert_one(team_data)  # 插入数据到集合
        return result.inserted_id  # 返回插入文档的 ID

    def find_team(self, team_id):
        """根据 TeamID 查找队伍信息"""
        return self.collection.find_one({"TeamID": team_id})

    def update_team(self, team_id, update_data):
        """更新指定队伍的信息"""
        return self.collection.update_one({"TeamID": team_id}, {"$set": update_data})

    def delete_team(self, team_id):
        """删除指定队伍的信息"""
        return self.collection.delete_one({"TeamID": team_id})
