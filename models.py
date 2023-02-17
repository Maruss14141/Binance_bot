import database


class User:
    def __init__(self, uid):
        self.uid = uid
        self.api_key = None
        self.secret_key = None

    def save_to_database(self):
        database.add_user(self.uid, self.api_key, self.secret_key)
