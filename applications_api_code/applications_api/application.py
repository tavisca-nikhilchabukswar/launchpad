import psycopg2
from configparser import ConfigParser
import sys

class tavisca_app:
    def __init__(self,form):
        self.app_name = None
        self.form = form
        self.app_instance_type = None
        self.app_instance_count = None
        self.app_env = None

    def database_config(self,filename='database.ini', section='postgresql'):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))   
        return db

    def create_db_connection(self):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # read connection parameters
            params = self.database_config()
    
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            # create a cursor
            cur = conn.cursor()
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
        # close the communication with the PostgreSQL
            return cur
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def store_app_in_database(self):
        try:
            db_connection = self.create_db_connection()
        except:
            print ("Unexpected error:", sys.exc_info()[0])
        finally:
            if db_connection is not None:
                db_connection.close()
                print('Database connection closed.')
