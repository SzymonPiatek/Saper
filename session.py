class Session:
    def __init__(self):
        self.logged_in = False
        self.user = None
        self.user_id = None
        self.user_username = None

    def login(self, username):
        self.logged_in = True
        self.user = username
        self.user_id = self.user[0]
        self.user_username = self.user[1]

    def logout(self):
        self.logged_in = False
        self.user = None
        self.user_id = None
        self.user_username = None
