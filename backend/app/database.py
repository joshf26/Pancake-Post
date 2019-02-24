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
                                "   username VARCHAR NOT NULL UNIQUE,"
                                "   hash VARCHAR NOT NULL,"
                                "   salt VARCHAR,"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE posts("
                                "   id SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   title VARCHAR,"
                                "   body VARCHAR,"
                                "   domain VARCHAR,"
                                "   created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP"
                                ")")
            self.cursor.execute("CREATE TABLE comments("
                                "   id SERIAL PRIMARY KEY,"
                                "   owner INTEGER NOT NULL,"
                                "   FOREIGN KEY (owner) REFERENCES users(id),"
                                "   post INTEGER,"
                                "   FOREIGN KEY (post) REFERENCES posts(id),"
                                "   body VARCHAR,"
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
            self.cursor.execute("CREATE TABLE commentVotes("
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

    # For adding and deleting posts
    def add_post(self, username, title, body, domain):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("INSERT INTO posts(owner, title, body, domain) "
                                "VALUES (%s, %s, %s, %s)",
                                (user_id, title, body, domain))
            return True
        return False

    def delete_post(self, post):
        self.cursor.execute("DELETE FROM posts WHERE id=%s", (post,))
        self.cursor.execute("DELETE FROM comments WHERE post=%s", (post,))

    # For adding and deleting comments
    def add_comment(self, username, post_id, body):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("INSERT INTO comments(owner, post, body) "
                                "VALUES (%s, %s, %s)",
                                (user_id, post_id, body))
            return True
        return False

    def delete_comment(self, comm):
        self.cursor.execute("DELETE FROM comments WHERE id=%s", (comm,))

    # For adding and deleting votes for posts
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
            self.cursor.execute("SELECT id from posts WHERE owner=%s AND post=%s",
                                (user_id, post))
            vote_id = self.cursor.fetchone()
            if vote_id:
                self.cursor.execute("DELETE FROM votes WHERE ID=%s", (vote_id,))
                return True

        return False

    # For adding and deleting votes for comments
    def add_vote_comments(self, username, comm):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("INSERT INTO commentVotes(owner, post) VALUES (%s, %s)", (user_id, comm))
            return True
        return False

    def delete_vote_comments(self, username, post):
        self.cursor.execute("SELECT id FROM users where username=%s", (username,))
        user_id = self.cursor.fetchone()

        if user_id:
            self.cursor.execute("SELECT id from posts WHERE owner=%s AND post=%s",
                                (user_id, post))
            vote_id = self.cursor.fetchone()
            if vote_id:
                self.cursor.execute("DELETE FROM commentVotes WHERE ID=%s", (vote_id,))
                return True

        return False

    def get_posts(self, domain, number, order):
        self.cursor.execute("SELECT * FROM posts WHERE domain=%s ORDER BY created_at DESC LIMIT " + str(number), (domain,))
        posts = self.cursor.fetchall()
        if posts:
            return [{
                'id': post[0],
                'owner': post[1],
                'owner_name': self.get_username_by_id(post[1]),
                'title': post[2],
                'body': post[3],
                'domain': post[4],
                'created_at': post[5]
            } for post in posts]

        return None

    def get_post_details(self, post_id):
        self.cursor.execute("SELECT * FROM posts WHERE id=%s", (post_id,))
        post = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM comments WHERE post=%s ORDER BY created_at DESC",
                            (post_id,))
        comments = self.cursor.fetchall()
        log(comments)
        return {
            'id': post[0],
            'owner': post[1],
            'owner_name': self.get_username_by_id(post[1]),
            'title': post[2],
            'body': post[3],
            'domain': post[4],
            'created_at': post[5],
            'comments': [{
                'id': comment[0],
                'owner': comment[1],
                'owner_name': self.get_username_by_id(comment[1]),
                'body': comment[3],
                'created_at': comment[4]
            } for comment in (comments if comments else [])]
        }

    # Edit this later
    def get_posts_from_user(self, domain, number, username):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = self.cursor.fetchone()
        if user_id:
        # TODO: We need to order these.
            self.cursor.execute("SELECT * FROM posts WHERE domain=%s AND owner=%s ORDER BY created_at DESC", (domain, user_id))
            posts = self.cursor.fetchall()
            if posts:
                return [{
                    'id': post[0],
                    'owner': post[1],
                    'title': post[2],
                    'body': post[3],
                    'domain': post[4],
                    'created_at': post[5]
                } for post in posts]

        return None

    def get_comments_of_user(self, username, domain):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username, ))
        user_id = self.cursor.fetchone()
        if user_id:
            self.cursor.execute("SELECT * FROM comments WHERE id=%s AND domain=%s ORDER BY created_at DESC", (user_id, domain))
            comments = self.cursor.fetchall()
            if comments:
                return [{
                    'id': post[0],
                    'owner': post[1],
                    'body': post[2],
                    'created_at': post[3]
                } for post in comments]
        return None

    # Edit this
    def get_upvotes(self, username, domain):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            self.cursor.execute("SELECT id FROM posts WHERE owner=%s AND domain=%s", (user_id, domain))
            post_id = self.cursor.fetchone()
            if post_id:
                self.cursor.execute("SELECT * FROM votes WHERE id=%s ORDER BY created_at DESC", (post_id,))
                comms = self.cursor.fetchall()
                if comms:
                    return [{
                        'owner': post[0],
                        'post': post[1],
                    } for post in post_id]
        return None

    def get_comment_upvotes(self, username, domain):
        self.cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user_id = self.cursor.fetchone()
        if user_id:
            self.cursor.execute("SELECT id FROM posts WHERE owner=%s AND domain=%s", (user_id, domain))
            post_id = self.cursor.fetchone()
            if post_id:
                self.cursor.execute("SELECT * FROM commentVotes WHERE id=%s ORDER BY created_at DESC", (post_id,))
                comms = self.cursor.fetchall()
                if comms:
                    return [{
                        'owner': post[0],
                        'post': post[1],
                    } for post in post_id]
        return None

    def get_username_by_id(self, id):
        self.cursor.execute("SELECT username FROM users where id=%s", (id,))
        username = self.cursor.fetchone()

        if username:
            return username[0]
