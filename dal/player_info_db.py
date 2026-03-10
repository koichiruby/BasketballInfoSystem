from pymongo import MongoClient

class PlayerDB:
    def __init__(self, db_url, db_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db['PlayerInfo']

    def add_player(self, player_data):
        return self.collection.insert_one(player_data).inserted_id

    def get_all_players(self):
        return list(self.collection.find({}))

    def update_player(self, player_id, update_data):
        return self.collection.update_one({"PlayerID": player_id}, {"$set": update_data})

    def get_player_by_id(self, player_id):#即find_player
        return self.collection.find_one({"PlayerID": player_id})


    def delete_player(self, player_id):
        return self.collection.delete_one({"PlayerID": player_id})
