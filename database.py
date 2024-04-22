import sqlite3


def create_users_table(conn):
    try:
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

def create_scores_table(conn):
    try:
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

def create_user(username, password):
    try:
        conn = sqlite3.connect("saper.db")
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO users (username, password)
            VALUES (?, ?)
            ''', (username, password)
        )
        conn.commit()
        print(f"Utworzono użytkownika {username}")
        return check_user(username=username, password=password)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def check_user(username, password):
    conn = sqlite3.connect("saper.db")
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT * FROM users WHERE username=? AND password=?
        ''', (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return user
    else:
        return False

def main():
    try:
        conn = sqlite3.connect('saper.db')
        print("Utworzono lub połączono z bazą danych 'saper.db'")

        create_users_table(conn)
        create_scores_table(conn)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
