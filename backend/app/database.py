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
            self.cursor.execute("SET TIMEZONE TO 'MST'")
            self.cursor.execute("CREATE TABLE users("
                                "   id SERIAL PRIMARY KEY,"
                                "   username VARCHAR NOT NULL UNIQUE,"
                                "   hash VARCHAR NOT NULL,"
                                "   salt VARCHAR,"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE posts("
                                "   id SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   parent INTEGER,"
                                "   FOREIGN KEY (parent) REFERENCES posts(id),"
                                "   title VARCHAR,"
                                "   body VARCHAR,"
                                "   domain VARCHAR,"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE votes("
                                "   id SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   post INTEGER NOT NULL,"
                                "   FOREIGN KEY (post) REFERENCES posts(id),"
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
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("INSERT INTO posts(owner, title, body, parent, domain) "
                                "VALUES (%s, %s, %s, %s, %s)",
                                (user_id, post_name, body, parent_id, domain))
            return True
        return False

    def delete_post(self, post):
        self.cursor.execute("DELETE FROM posts WHERE id=%s", (post,))

    def add_vote(self, username, post):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("INSERT INTO votes(owner, post) VALUES (%s, %s)", (user_id, post))
            return True
        return False

    def delete_vote(self, username, post):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("SELECT id from posts WHERE owner=%s AND parent=%s",
                                (user_id, post))
            vote_id = self.cursor.fetchone()
            if vote_id:
                self.cursor.execute("DELETE FROM votes WHERE ID=%s", (vote_id,))
                return True

        return False

    def get_posts(self, domain, number, order):
        # TODO: We need to order these.
        self.cursor.execute("SELECT * FROM posts WHERE domain=%s LIMIT " + str(number), (domain,))
        posts = self.cursor.fetchall()
        if posts:
            return [{
                'id': post[0],
                'owner': post[1],
                'owner_name': self.get_username_by_id(post[1]),
                'parent': post[2],
                'title': post[3],
                'body': post[4],
                'domain': post[5],
                'created_at': post[6]
            } for post in posts]

        return None

    def get_replies(self, username, title):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            self.cursor.execute("SELECT id FROM posts WHERE title=%s", (title,))
            post_id = self.cursor.fetchone()
            if post_id:
                self.cursor.execute("SELECT * FROM posts WHERE parent=%s", (post_id,))
                posts = self.cursor.fetchall()
                return [{
                    'id': post[0],
                    'owner': post[1],
                    'parent': post[2],
                    'title': post[3],
                    'body': post[4],
                    'domain': post[5],
                    'created_at': post[6]
                } for post in posts]

    def get_username_by_id(self, id):
        self.cursor.execute("SELECT username FROM users where id=%s", (id,))
        username = self.cursor.fetchone()

        if username:
            return username[0]
