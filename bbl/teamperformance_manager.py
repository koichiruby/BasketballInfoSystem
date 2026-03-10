from dal.team_performance_db import TeamPerformanceDB

class TeamPerformanceManager:
    def __init__(self, db_url, db_name):
        # 初始化数据库访问层实例
        self.db = TeamPerformanceDB(db_url, db_name)

    def add_team_performance(self, performance_data):
        """
        添加新的队伍表现信息。
        :param performance_data: dict, 包含队伍表现的基本信息
        :return: 新添加文档的ID
        """
        # 验证必要字段
        required_fields = ["MatchID", "Date", "TeamID", "TeamName", "TeamType", "Score", "MatchResult"]
        for field in required_fields:
            if field not in performance_data:
                raise ValueError(f"缺少必要字段：{field}")

        # 检查是否已存在相同 TeamID 和 MatchID 的记录
        existing = self.db.find_team_performance(performance_data["TeamID"], performance_data["MatchID"])
        if existing:
            raise ValueError("该队伍在该场比赛的表现记录已存在")

        # 插入新记录
        return self.db.add_team_performance(performance_data)

    def get_team_performance(self, team_id, match_id):
        """
        获取指定队伍在指定比赛中的表现信息。
        :param team_id: str, 队伍唯一标识
        :param match_id: str, 比赛唯一标识
        :return: 表现记录的字典数据
        """
        performance = self.db.find_team_performance(team_id, match_id)
        if not performance:
            raise ValueError("未找到该队伍在该场比赛的表现记录")
        return performance

    def update_team_performance(self, team_id, match_id, update_data):
        """
        更新队伍在指定比赛中的表现信息。
        :param team_id: str, 队伍唯一标识
        :param match_id: str, 比赛唯一标识
        :param update_data: dict, 需要更新的数据
        :return: 更新操作的结果
        """
        existing = self.db.find_team_performance(team_id, match_id)
        if not existing:
            raise ValueError("未找到该队伍在该场比赛的表现记录，无法更新")

        # 更新记录
        return self.db.update_team_performance(team_id, match_id, update_data)

    def delete_team_performance(self, team_id, match_id):
        """
        删除队伍在指定比赛中的表现信息。
        :param team_id: str, 队伍唯一标识
        :param match_id: str, 比赛唯一标识
        :return: 删除操作的结果
        """
        existing = self.db.find_team_performance(team_id, match_id)
        if not existing:
            raise ValueError("未找到该队伍在该场比赛的表现记录，无法删除")

        # 删除记录
        return self.db.delete_team_performance(team_id, match_id)
