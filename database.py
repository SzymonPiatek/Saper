import sqlite3

class Database:
    def __init__(self):
        self.db_name = "saper.db"

    def create_users_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                    )
                '''
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_scores_table(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    difficulty_level INTEGER,
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                '''
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO users (username, password)
                VALUES (?, ?)
                ''', (username, password)
            )
            conn.commit()
            return self.check_user(username=username, password=password)
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def insert_score(self, user_id, difficulty_level, score):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                '''
                INSERT INTO scores (user_id, difficulty_level, score)
                VALUES (?, ?, ?)
                ''', (user_id, difficulty_level, score)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_user_by_id(self, id=0):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                '''
                SELECT * FROM users 
                WHERE id=?
                ''', (id,)
            )
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def get_scores(self, amount, player=False, difficulty_level=0):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            if not player:
                cursor.execute(
                    '''
                    SELECT * FROM scores 
                    WHERE difficulty_level=?
                    ORDER BY score ASC
                    LIMIT ?
                    ''', (difficulty_level, amount,)
                )
            else:
                cursor.execute(
                    '''
                    SELECT * FROM scores 
                    WHERE difficulty_level=? AND user_id=?
                    ORDER BY score ASC
                    LIMIT ?
                    ''', (difficulty_level, player, amount,)
                )
            scores = cursor.fetchall()
            return scores
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()



    def check_user(self, username, password):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute(
                '''
                SELECT * FROM users WHERE username=? AND password=?
                ''', (username, password)
            )
            user = cursor.fetchone()
            return user
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def initialize_database(self):
        try:
            self.create_users_table()
            self.create_scores_table()
        except sqlite3.Error as e:
            print(e)
