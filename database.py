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
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                    )
                '''
            )
            conn.commit()
            print("Utworzono tabelę użytkowników")
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
                    score INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                '''
            )
            conn.commit()
            print("Utworzono tabelę wyników")
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
            print(f"Utworzono użytkownika {username}")
            return self.check_user(username=username, password=password)
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
