import sqlite3
import logging

class Db(object):

    __db_path = "" #TODO move to configuration file and limit permissions

    def connect(self):
        logging.info("DB: connecting")
        try:
            self.connect = sqlite3.connect(Db.__db_path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as err
            logging.error("DB: could not connect\n" + err.message)

    def close(self):
        logging.info("DB: closing")
        self.connection.close()

    def execute(self, query):
        logging.info("DB: executing query \n\t" + str(query))
        self.cur.execute(quert)

    def commit(self):
        logging.info("DB: commiting changes")
        self.connection.commit()
