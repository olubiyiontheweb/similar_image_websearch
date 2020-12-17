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
            'CREATE TABLE IF NOT EXISTS image_store_hash (image_hash_id INTEGER PRIMARY KEY AUTOINCREMENT, image_hash TEXT UNIQUE, image_id INTEGER, FOREIGN KEY (image_id) REFERENCES image_store (image_id) )'
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
        try:
            table_values = str(table_values)[1:-1]
            conn.execute("INSERT INTO " + table_name + " VALUES(null, " +
                         table_values + ")")
            conn.commit()
            print("Values inserted successfully")
        except:
            conn.rollback()
            print("error in insert operation")

        conn.close()

    def request_matches(self, table_name):
        conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute( \
            "select * from " + table_name
        )

        json = cur.fetchall()
        print("this is it" + str(json))
        return json

    def conditional_request_matches(self, table_name, by_value,
                                    select_col_name, where_col_name):
        conn = sqlite3.connect('.\\database\\database.db')
        print("Opened database successfully")
        cur = conn.cursor()
        # print("select " + select_col_name + " from " + table_name + " where " +
        #      where_col_name + " = " + by_value)
        cur.execute("select " + select_col_name + " from " + table_name +
                    " where " + where_col_name + " = " + str(by_value))

        list = cur.fetchall()
        print("this is it" + str(list))
        return list