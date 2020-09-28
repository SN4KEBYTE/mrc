import sqlite3


# todo: i don't really understand, how does it works. And i think that there are some errors here.
class ReviewDB:
    def __init__(self, db_path) -> None:
        self.__conn: sqlite3.Connection = sqlite3.connect(db_path)
        self.__cur: sqlite3.Cursor = self.__conn.cursor()

    def create(self) -> None:
        self.__cur.execute('CREATE TABLE review_db (review TEXT, sentiment INTEGER, date TEXT)')

        self.__conn.commit()
        self.__conn.close()

    def insert_entry(self, document, label):
        self.__cur.execute('INSERT INTO review_db (review, sentiment, date) VALUES (?, ?, DATETIME("now"))',
                           (document, label))
