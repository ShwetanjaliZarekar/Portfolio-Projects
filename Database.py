import sqlite3
from Data_Collection import user_data


def InsertCreateDatabase():
    try:
        sqliteConnection = sqlite3.connect('GitHub.db')
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS GitHub (id INTEGER PRIMARY KEY,username TEXT,email TEXT,followers INTEGER,type TEXT,number_of_repos
        INTEGER,achievements INTEGER,languages TEXT);'''

        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        cursor.execute(sqlite_create_table_query)


        sql = '''INSERT INTO GitHub (username, email, followers, type,number_of_repos, achievements,languages)
             VALUES (?, ?, ?, ?, ?, ?, ?)'''

        values = [(user['username'], user['email'], user['followers'], user['type'], user['number of repos'],
                   user['achievements'], user['languages']) for user in user_data]

        cursor.executemany(sql, values)

        print("Total", cursor.rowcount, "Records inserted successfully into git table")

        # Select all rows from the users table
        cursor.execute('''SELECT * FROM GitHub''')
        rows = cursor.fetchall()

        for row in rows:
            print(row)

        sqliteConnection.commit()
        print("SQLite table created")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
