import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from conf import *
from helper import log
from auth import generate_hash


class Database:

    def __init__(self):
        log('Initializing database...')

        self.connection = psycopg2.connect(host='database', user='postgres')
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

        # Check if the database exists.
        self.cursor.execute(f"SELECT * FROM pg_catalog.pg_database "
                            f"WHERE datname = '{DATABASE_NAME}';")

        needs_tables = False
        if not self.cursor.fetchone():
            # The database does not exist, so create one now.
            log('Creating database...')
            self.cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
            needs_tables = True

        # Switch to the correct table.
        self.cursor.close()
        self.connection.close()
        self.connection = psycopg2.connect(host='database', user='postgres', database=DATABASE_NAME)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

        # Create the tables is needed.
        if needs_tables:
            self.cursor.execute("CREATE TABLE users(ID SERIAL PRIMARY KEY, Username varchar(255) NOT NULL UNIQUE, Password varchar(255) NOT NULL, salt int,created_at TIMESTAMP WITH TIME ZONE MST CURRENT_TIMESTAMP")
            self.cursor.execute("CREATE TABLE posts(ID SERIAL PRIMARY KEY, FOREIGN KEY (uid) REFERENCES users(uid),Title varchar(255), Content varchar(255), FOREIGN KEY (parent) REFERENCES posts(parent)), domain varchar(255), created_at TIMESTAMP WITH TIME ZONE MST CURRENT_TIMESTAMP")
            self.cursor.execute("CREATE TABLE votes(ID SERIAL PRIMARY KEY, FOREIGN KEY (uid) REFERENCES users(uid), FOREIGN KEY (parent) REFERENCES posts(parent), created_at TIMESTAMP WITH TIME ZONE MST CURRENT_TIMESTAMP")
            

        log(f'Database initialized! Name: {DATABASE_NAME}')

    def create_user(self, username, password):
        pw_hash, salt = generate_hash(password)
        self.cursor.execute("INSERT INTO users(username, password, salt) VALUES (%s, %s, %s)", (username, pw_hash, salt))
        
    def add_comment(self, post_name, content, parent_id, user_id, domain):
        if(parent_id == -1):
            parent_id = None
        self.cursor.execute("INSERT INTO posts(uid, title, content, parent, site) VALUES (%s, %s, %s, %s, %s)", (user_id, post_name, content, parent_id, domain))

    def delete_comment(self, post_id):
        self.cursor.execute("DELETE FROM posts WHERE ID=%s", (post_id))

