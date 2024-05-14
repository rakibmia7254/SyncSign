import sqlite3
import uuid

class SQLDB:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.add_default_data()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT,
                _id TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                app_id TEXT,
                user_id TEXT,
                _id TEXT,
                expires INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS apps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                redirect_uri TEXT,
                api_key TEXT,
                logo TEXT,
                _id TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_tokens (
                code TEXT NOT NULL,
                app_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                email TEXT NOT NULL,
                expires REAL NOT NULL,
                _id TEXT NOT NULL,
                access_token TEXT NOT NULL,
                PRIMARY KEY (_id)
            )
        ''')
        self.conn.commit()

    def fetch_json(self, query, args=()):
        self.cursor.execute(query, args)
        columns = [col[0] for col in self.cursor.description]
        data = self.cursor.fetchall()
        return [dict(zip(columns, row)) for row in data]
    
    def add_default_data(self):
        if not self.fetch_json('SELECT * FROM admin'): self.set_admin('admin', 'admin')

    def get_admin(self, username):
        query = 'SELECT * FROM admin WHERE username = ?'
        if self.fetch_json(query, (username,)): return self.fetch_json(query, (username,))[0]
        return {}

    def set_admin(self, username, password):
        self.cursor.execute('INSERT INTO admin (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def update_admin(self, id, username, password):
        self.cursor.execute('UPDATE admin SET username = ?, password = ? WHERE id = ?', (username, password, id))
        self.conn.commit()

    def get_user(self, email):
        query = 'SELECT * FROM users WHERE email = ?'
        if self.fetch_json(query, (email,)): return self.fetch_json(query, (email,))[0]
        return {}
    
    def get_users(self):
        query = 'SELECT * FROM users'
        return self.fetch_json(query)

    def get_user_by_id(self, _id):
        query = 'SELECT email, _id FROM users WHERE _id = ?'
        if self.fetch_json(query, (_id,)): return self.fetch_json(query, (_id,))[0]
        return {}

    def set_user(self, email, password, _id=uuid.uuid4().hex):
        self.cursor.execute('INSERT INTO users (email, password, _id) VALUES (?, ?, ?)', (email, password, _id))
        self.conn.commit()

    def delete_user(self, id):
        self.cursor.execute('DELETE FROM users WHERE _id = ?', (id,))
        self.conn.commit()

    def add_data(self, data):
        self.cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (data['email'], data['password']))
        self.conn.commit()

    def add_code(self, code):
        app_id = code['app_id']
        user_id = code['user_id']
        expires = code['expires']
        self.cursor.execute('INSERT INTO codes (code, app_id, user_id, _id, expires) VALUES (?, ?, ?, ?, ?)', (code['code'], app_id, user_id, uuid.uuid4().hex, expires))
        self.conn.commit()

    def get_code(self, code):
        query = 'SELECT * FROM codes WHERE code = ?'
        if self.fetch_json(query, (code,)):
            return self.fetch_json(query, (code,))[0]
        return {}

    def delete_code(self, code):
        self.cursor.execute('DELETE FROM codes WHERE code = ?', (code,))
        self.conn.commit()

    def add_app(self, app):
        app['_id'] = uuid.uuid4().hex
        name = app['name']
        api_key = app['api_key']
        logo = app['logo']
        redirect_uri = app['redirect_uri']

        self.cursor.execute('INSERT INTO apps (name, api_key, logo, redirect_uri, _id) VALUES (?, ?, ?, ?, ?)', (name, api_key, logo, redirect_uri, app['_id']))
        self.conn.commit()

    def get_app(self, app_id):
        query = 'SELECT * FROM apps WHERE _id = ?'
        if self.fetch_json(query, (app_id,)):
            return self.fetch_json(query, (app_id,))[0]
        return {}

    def get_app_by_id(self, _id):
        query = 'SELECT * FROM apps WHERE _id = ?'
        if self.fetch_json(query, (_id,)):
            return self.fetch_json(query, (_id,))[0]
        return {}

    def get_apps(self):
        query = 'SELECT * FROM apps'
        return self.fetch_json(query)

    def update_app(self, app_id, app):
        name = app['name']
        redirect_uri = app['redirect_uri']
        self.cursor.execute('UPDATE apps SET name = ?, redirect_uri = ? WHERE _id = ?', (name, redirect_uri, app_id))
        self.conn.commit()

    def delete_app(self, app_id):
        self.cursor.execute('DELETE FROM apps WHERE id = ?', (app_id,))
        self.conn.commit()

    def add_access_token(self, token, email="none"):
    
        self.cursor.execute('INSERT INTO access_tokens (code, app_id, user_id, email, expires, _id, access_token) VALUES (?, ?, ?, ?, ?, ?, ?)', (
            "userlog",
            token['app_id'],
            token['user_id'],
            email,
            token['expires'],
            token['_id'],
            token['access_token']
        ))
        self.conn.commit()

    def get_access_token(self, token):
        query = 'SELECT * FROM access_tokens WHERE access_token = ?'
        if self.fetch_json(query, (token,)):
            return self.fetch_json(query, (token,))[0]
        return {}
    
    def get_access_token_by_id(self, user_id):
        query = 'SELECT * FROM access_tokens WHERE user_id = ?'
        if self.fetch_json(query, (user_id,)):
            return self.fetch_json(query, (user_id,))[0]
        return {}

    def delete_access_token(self, token):
        self.cursor.execute('DELETE FROM access_tokens WHERE access_token = ?', (token,))
        self.conn.commit()
    
    def exec_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
