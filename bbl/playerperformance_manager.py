from dal.player_performance_db import PlayerPerformanceDB

class Player_PerformanceManager:
    def __init__(self, db_url, db_name):
        # 初始化数据库访问层实例
        self.db = PlayerPerformanceDB(db_url, db_name)

    def add_performance(self, performance_data):
        """
        添加新的比赛表现记录。
        :param performance_data: dict，包含比赛表现的信息
        :return: 新添加文档的ID
        """
        # 验证必要字段
        required_fields = ["PlayerID", "Matchid", "Date", "Score", "Assists"]
        for field in required_fields:
            if field not in performance_data:
                raise ValueError(f"缺少必要字段：{field}")

        # 检查是否已存在相同 PlayerID 和 Matchid 的记录
        existing = self.db.find_performance(performance_data["PlayerID"], performance_data["Matchid"])
        if existing:
            raise ValueError("该球员在该场比赛的表现记录已存在")

        # 插入新记录
        return self.db.add_performance(performance_data)

    def get_performance(self, player_id, match_id):
        """
        获取指定球员在指定比赛中的表现记录。
        :param player_id: str，球员唯一标识
        :param match_id: str，比赛唯一标识
        :return: 表现记录的字典数据
        """
        performance = self.db.find_performance(player_id, match_id)
        if not performance:
            raise ValueError("未找到该球员在该场比赛的表现记录")
        return performance

    def update_performance(self, player_id, match_id, update_data):
        """
        更新球员在指定比赛中的表现。
        :param player_id: str，球员唯一标识
        :param match_id: str，比赛唯一标识
        :param update_data: dict，需要更新的数据
        :return: 更新操作的结果
        """
        existing = self.db.find_performance(player_id, match_id)
        if not existing:
            raise ValueError("未找到该球员在该场比赛的表现记录，无法更新")

        # 更新记录
        return self.db.update_performance(player_id, match_id, update_data)

    def delete_performance(self, player_id, match_id):
        """
        删除球员在指定比赛中的表现记录。
        :param player_id: str，球员唯一标识
        :param match_id: str，比赛唯一标识
        :return: 删除操作的结果
        """
        existing = self.db.find_performance(player_id, match_id)
        if not existing:
            raise ValueError("未找到该球员在该场比赛的表现记录，无法删除")

        # 删除记录
        return self.db.delete_performance(player_id, match_id)
