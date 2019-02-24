import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from conf import *
from helper import log
from auth import generate_hash, check_password


class Orders:
    VOTES = ''
    RECENT = ''


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

        # Create the tables if needed.
        if needs_tables:
            self.cursor.execute("SET TIMEZONE TO 'GMT'")
            self.cursor.execute("CREATE TABLE users("
                                "   id SERIAL PRIMARY KEY,"
                                "   username VARCHAR(255) NOT NULL UNIQUE,"
                                "   hash VARCHAR(255) NOT NULL,"
                                "   salt VARCHAR(255),"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE posts("
                                "   id SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   parent INTEGER,"
                                "   FOREIGN KEY (parent) REFERENCES posts(id),"
                                "   title VARCHAR(255),"
                                "   body VARCHAR(255),"
                                "   domain VARCHAR(255),"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE votes("
                                "   ID SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   post INTEGER NOT NULL,"
                                "   FOREIGN KEY (parent) REFERENCES posts(id),"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")

        log(f'Database initialized! Name: {DATABASE_NAME}')

    def create_user(self, username, password):
        pw_hash, salt = generate_hash(password)
        self.cursor.execute("SELECT hash, salt FROM users WHERE username=%s", (username,))

        pw_information = self.cursor.fetchone()
        if pw_information:
            return False

        self.cursor.execute("INSERT INTO users(username, hash, salt) "
                            "VALUES (%s, %s, %s)", (username, pw_hash, salt))

        return True

    def check_user(self, username, password):
        self.cursor.execute("SELECT hash, salt FROM users WHERE username=%s", (username,))
        pw_information = self.cursor.fetchone()

        if pw_information:
            pw_hash, salt = pw_information
            return check_password(password, pw_hash, salt)

        return False

    def add_post(self, username, post_name, body, parent_id, domain):
        # TODO: We need to look up the user id by username
        # self.cursor.execute("INSERT INTO posts(uid, title, body, parent, site) "
        #                     "VALUES (%s, %s, %s, %s, %s)",
        #                     (user_id, post_name, body, parent_id, domain))
        pass

    def delete_post(self, post):
        self.cursor.execute("DELETE FROM posts WHERE id=%s", (post))
        self.cursor.execute("DELETE FROM votes WHERE parent=%s", (post))

    def add_vote(self, username, post):
        # TODO: We need to look up the user id by username
        # self.cursor.execute("INSERT INTO votes(owner, post) VALUES (%s, %s)", (username, post))
        pass

    def delete_vote(self, username, post):
        # TODO: We need to look up the user id by username
        # self.cursor.execute("DELETE FROM votes WHERE ID=%s", vote_id)
        pass

    def get_posts(self, domain, number, order):
        # TODO: Ordered by "order".
        self.cursor.execute("SELECT * FROM posts WHERE domain=%s LIMIT " + str(number), (domain,))
        posts = self.cursor.fetchall()
        if posts:
            return posts
        return 'No Posts :('
