import sqlite3


class database_migrations:
    # def __init__(self):
    #     self.conn = sqlite3.connect('.\\database\\database.db')
    #     print("Opened database successfully")

    def image_store_migrations(self):
        conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")
        print("Creating database tables ....")
        conn.execute( \
            'CREATE TABLE IF NOT EXISTS image_store (image_id INTEGER PRIMARY KEY AUTOINCREMENT, image_name TEXT UNIQUE, storage_location TEXT, storage_service TEXT)'
        )
        conn.execute( \
            'CREATE TABLE IF NOT EXISTS image_store_hash (image_hash_id INTEGER PRIMARY KEY AUTOINCREMENT, image_hash TEXT, image_id INTEGER, FOREIGN KEY (image_id) REFERENCES image_store (image_id) )'
        )
        conn.execute( \
            'CREATE TABLE IF NOT EXISTS person_details (person_id INTEGER PRIMARY KEY AUTOINCREMENT, person_name TEXT)')
        conn.execute( \
            'CREATE TABLE IF NOT EXISTS faces_in_store (faces_id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, image_id INTEGER, image_hash_id INTEGER, FOREIGN KEY (person_id) REFERENCES person_details (person_id), FOREIGN KEY (image_id) REFERENCES image_store (image_id), FOREIGN KEY (image_hash_id) REFERENCES image_store_hash (image_hash_id))'
        )
        print("Table created successfully")
        conn.close()

    def insert_operations(self, table_name, table_values):
        conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")
        print("Inserting values in database tables ....")
        print(table_values["image_name"])
        print(table_values["storage_service"])
        try:
            conn.execute( \
            "INSERT INTO " + table_name + "(image_name,storage_location,storage_service) VALUES (?,?,?)",
            (table_values["image_name"], table_values["storage_location"], table_values["storage_service"])
            )
            conn.commit()
            print("Values inserted successfully")
        except:
            conn.rollback()
            print("error in insert operation")

        conn.close()

    def request_matches(self):
        conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute( \
            "select * from image_store"
        )

        json = cur.fetchall()
        print("this is it" + str(json))
        return json