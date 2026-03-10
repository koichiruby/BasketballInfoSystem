from dal.player_info_db import PlayerDB
#从 dal 文件夹中的 player_db.py 文件中导入 PlayerDB 类。

class PlayerInfo_Manager:
    def __init__(self, db_url, db_name):
        self.db = PlayerDB(db_url, db_name)

    def add_player(self, player_data):
        # 检查数据完整性并添加球员
        required_fields = ["PlayerID", "Name", "TeamID", "Number", "Position"]
        for field in required_fields:
            if field not in player_data:
                raise ValueError(f"缺少必要字段：{field}")
        return self.db.add_player(player_data)

    def get_all_players(self):
        return self.db.get_all_players()

    def update_player(self, player_id, update_data):
        return self.db.update_player(player_id, update_data)


    def get_player_by_id(self, player_id):
        """根据 PlayerID 查询球员"""
        return self.db.get_player_by_id( player_id)

    def delete_player(self, player_id):
        return self.db.delete_player(player_id)
