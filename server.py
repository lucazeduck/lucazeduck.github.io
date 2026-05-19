import flask
import sqlite3
import random
import os
import hashlib

app = flask.Flask(__name__)

# Initialize database
DB_PATH = os.path.join(os.path.dirname(__file__), 'speedcube.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS solves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                time_ms INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_username(username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

def create_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        try:
            password_hash = hash_password(password)
            cursor = conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None

def verify_user(username, password):
    user = get_user_by_username(username)
    if user and user[2] == hash_password(password):
        return user[0]  # Return user_id
    return None

def get_user_solves(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('SELECT time_ms FROM solves WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        return [row[0] for row in cursor.fetchall()]

def add_solve(user_id, time_ms):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('INSERT INTO solves (user_id, time_ms) VALUES (?, ?)', (user_id, time_ms))
        conn.commit()
        return True

def get_leaderboard(limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT u.username, s.time_ms 
            FROM solves s 
            JOIN users u ON s.user_id = u.id 
            ORDER BY s.time_ms ASC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

def get_user_leaderboard(user_id, limit=10):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute('''
            SELECT u.username, s.time_ms 
            FROM solves s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.user_id = ? 
            ORDER BY s.time_ms ASC 
            LIMIT ?
        ''', (user_id, limit))
        return cursor.fetchall()

def clear_user_data(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM solves WHERE user_id = ?', (user_id,))
        conn.commit()
        return True

def generate_scramble():
    faces = ['U', 'D', 'F', 'B', 'L', 'R']
    moves = []
    last_face = None
    for _ in range(20):
        face = random.choice(faces)
        while face == last_face:
            face = random.choice(faces)
        modifier = random.choice(["", "'", "2"])
        moves.append(face + modifier)
        last_face = face
    return " ".join(moves)

@app.route('/')
def index():
    scramble = generate_scramble()
    leaderboard = get_leaderboard()
    return flask.render_template('index.html', scramble=scramble, leaderboard=leaderboard)

@app.route('/api/scramble')
def api_scramble():
    return flask.jsonify({'scramble': generate_scramble()})

@app.route('/api/leaderboard')
def api_leaderboard():
    leaderboard = get_leaderboard()
    formatted = [{'name': row[0], 'time': row[1]} for row in leaderboard]
    return flask.jsonify(formatted)

@app.route('/api/user/leaderboard/<int:user_id>')
def api_user_leaderboard(user_id):
    leaderboard = get_user_leaderboard(user_id)
    formatted = [{'name': row[0], 'time': row[1]} for row in leaderboard]
    return flask.jsonify(formatted)

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = flask.request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return flask.jsonify({'success': False, 'error': 'Missing username or password'}), 400
    user_id = create_user(username, password)
    if user_id:
        return flask.jsonify({'success': True, 'user_id': user_id, 'username': username})
    return flask.jsonify({'success': False, 'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = flask.request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return flask.jsonify({'success': False, 'error': 'Missing username or password'}), 400
    user_id = verify_user(username, password)
    if user_id:
        solves = get_user_solves(user_id)
        user_lb = get_user_leaderboard(user_id)
        return flask.jsonify({
            'success': True, 
            'user_id': user_id, 
            'username': username,
            'solves': solves,
            'leaderboard': [{'name': row[0], 'time': row[1]} for row in user_lb]
        })
    return flask.jsonify({'success': False, 'error': 'Invalid username or password'}), 401

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = flask.request.json
    user_id = data.get('user_id')
    time_ms = data.get('time_ms')
    if user_id and time_ms:
        add_solve(user_id, time_ms)
        return flask.jsonify({'success': True})
    return flask.jsonify({'success': False, 'error': 'Missing data'}), 400

@app.route('/api/clear', methods=['POST'])
def api_clear():
    data = flask.request.json
    user_id = data.get('user_id')
    if user_id:
        clear_user_data(user_id)
        return flask.jsonify({'success': True})
    return flask.jsonify({'success': False, 'error': 'Missing user_id'}), 400

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
