from dal.match_info_db import MatchInfoDB

class MatchInfoManager:
    def __init__(self, db_url, db_name):
        # 初始化数据库访问层实例
        self.db = MatchInfoDB(db_url, db_name)
    def get_all_matches(self):
        return self.db.get_all_matches()
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
        existing = self.db.find_match_info(match_data["MatchID"])
        if existing:
            raise ValueError("该场比赛记录已存在")

        # 插入新记录
        return self.db.add_match_info(match_data)

    def get_match_info(self, match_id):
        """
        获取指定比赛的信息。
        :param match_id: str, 比赛唯一标识
        :return: 比赛信息的字典数据
        """
        match_info = self.db.find_match_info(match_id)
        if not match_info:
            raise ValueError("未找到该场比赛的信息")
        return match_info

    def update_match(self, match_id, update_data):
        """
        更新指定比赛的信息。
        :param match_id: str, 比赛唯一标识
        :param update_data: dict, 需要更新的数据
        :return: 更新操作的结果
        """
        existing = self.db.find_match_info(match_id)
        if not existing:
            raise ValueError("未找到该场比赛的信息，无法更新")

        # 更新记录
        return self.db.update_match_info(match_id, update_data)

    def delete_match(self, match_id):
        """
        删除指定比赛的信息。
        :param match_id: str, 比赛唯一标识
        :return: 删除操作的结果
        """
        existing = self.db.find_match_info(match_id)
        if not existing:
            raise ValueError("未找到该场比赛的信息，无法删除")

        # 删除记录
        return self.db.delete_match_info(match_id)
    def get_match_by_id(self, match_id):

        return self.db.get_match_by_id( match_id)
