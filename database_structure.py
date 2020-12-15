import sqlite3


class database_migrations:
    def __init__(self):
        self.conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")

    def image_store_migrations(self):
        self.conn.execute(
            'CREATE TABLE image_store (file_name TEXT, storage_location TEXT, storage_service TEXT)'
        )
        print("Table created successfully")
        self.conn.close()

    def request_matches(self):
        return "success"