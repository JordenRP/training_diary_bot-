import sqlite3

class Db:
    def __init__(self, name):
        self.name =  name
        self.id = -1

        self.create_db()

    def create_db(self):
        db = sqlite3.connect(self.name + '.db')
        cursor = db.cursor()

        cursor.execute('''create table if not exists exercise 
            (id INTEGER PRIMARY KEY NOT NULL, name TEXT, weight INTEGER,rep INTEGER)''')

        db.commit()
        db.close()

    def create_field(self):
        db = sqlite3.connect(self.name + '.db')
        cursor = db.cursor()

        cursor.execute('INSERT INTO exercise (name, weight, rep) VALUES("", "", "")')
            
        db.commit()
        db.close()

        self.set_last_id()

    def set_last_id(self):
        db = sqlite3.connect('test.db')
        cursor = db.cursor()

        cursor.execute('SELECT id FROM exercise order by id DESC LIMIT 1')
        self.id = cursor.fetchone()[0]


    def save_name(self, name: str):
        if self.id == -1:
            raise MyError("ID not set")

        db = sqlite3.connect(self.name + '.db')
        cursor = db.cursor()
        
        params = (name, self.id)

        cursor.execute(
            f"UPDATE exercise "
            f"SET name = ? "
            f"WHERE "
            f"id = ?;"
        , params)

        db.commit()
        db.close()

    def save_weight(self, weight: int):
        if self.id == -1:
            raise MyError("ID not set")

        db = sqlite3.connect(self.name + '.db')
        cursor = db.cursor()

        params = (weight, self.id)

        cursor.execute(
            f"UPDATE exercise "
            f"SET weight = ? "
            f"WHERE "
            f"id = ?;"
        , params)

        db.commit()
        db.close()

    def save_rep(self, rep: int): 
        if self.id == -1:
            raise MyError("ID not set")

        db = sqlite3.connect(self.name + '.db')
        cursor = db.cursor()

        params = (rep, self.id)

        cursor.execute(
            f"UPDATE exercise "
            f"SET rep = ? "
            f"WHERE id = ?;"
        , params)

        db.commit()
        db.close()

