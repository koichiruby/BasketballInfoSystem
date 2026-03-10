from dal.team_info_db import TeamDB

class TeamInfo_Manager:
    def __init__(self, db_url, db_name):
        self.db = TeamDB(db_url, db_name)


    def add_team(self, team_data):
        """
        添加新团队。
        :param team_data: dict 包含团队的信息
        :return: 新添加文档的ID
        """
        # 验证必要字段
        required_fields = ["TeamID", "TeamName", "members"]
        for field in required_fields:
            if field not in team_data:
                raise ValueError(f"缺少必要字段：{field}")

        # 检查是否已存在相同 TeamID 的记录
        existing = self.db.get_team_by_id(team_data["TeamID"])
        if existing:
            raise ValueError("该团队已存在")

        # 插入新记录
        return self.db.add_team(team_data)

    def get_team(self, team_id):
        """
        获取团队信息。
        :param team_id: str，团队唯一标识
        :return: 团队记录的字典数据
        """
        team = self.db.get_team_by_id(team_id)
        if not team:
            raise ValueError("未找到该团队的信息")
        return team

    def get_all_teams(self):
        """
        获取所有团队信息
        :return: 所有球队的列表
        """
        return list(self.db.collection.find())

    def get_team_by_id(self, team_id):
        """
        获取指定 TeamID 的团队信息
        :param team_id: 团队的唯一标识符
        :return: 返回团队数据或 None
        """
        return self.db.get_team_by_id(team_id)  # 调用 TeamDB 中的查询方法

    def update_team(self, team_id, update_data):
        """
        更新团队信息。
        :param team_id: str，团队唯一标识
        :param update_data: dict，需要更新的数据
        :return: 更新操作的结果
        """
        existing = self.db.get_team_by_id(team_id)
        if not existing:
            raise ValueError("未找到该团队的信息，无法更新")

        # 更新记录
        return self.db.update_team(team_id, update_data)

    def delete_team(self, team_id):
        """
        删除团队记录。
        :param team_id: str，团队唯一标识
        :return: 删除操作的结果
        """
        existing = self.db.get_team_by_id(team_id)
        if not existing:
            raise ValueError("未找到该团队的信息，无法删除")

        # 删除记录
        return self.db.delete_team(team_id)
