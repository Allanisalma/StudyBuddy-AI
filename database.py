import sqlite3
DATABASE_NAME = "StudyBuddy.db"
def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            content TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            subject TEXT
        )
    """)
    connection.commit()
    connection.close()
def add_task(title, subject, due_date):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO study_tasks
        (title, subject, due_date, user_id)
        VALUES (?, ?, ?, ?)
    """, (title, subject, due_date))
    connection.commit()
    connection.close()
def get_tasks():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM study_tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    connection.close()
    return tasks
def update_task_status(task_id, completed):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("UPDATE study_tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
    connection.commit()
    connection.close()
def delete_task(task_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM study_tasks WHERE id = ?", (task_id))
    connection.commit()
    connection.close()
def fix_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(study_tasks)")
    columns = [row[1] for row in cursor.fetchall()]
    if columns and "due_date" not in columns:
        cursor.execute("ALTER TABLE study_tasks ADD COLUMN due_date TEXT")
    connection.commit()
    connection.close()
def update_task_status(task_id, completed):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("UPDATE study_tasks SET completed = ? WHERE id = ?", (1 if completed else 0, task_id))
    connection.commit()
    connection.close()
def create_notes_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()
def add_note(title, subject, content):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO study_notes (title, subject, content)
        VALUES (?, ?, ?)
    """, (title, subject, content))
    connection.commit()
    connection.close()
def get_notes():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM study_notes ORDER BY id DESC")
    notes = cursor.fetchall()
    connection.close()
    return notes
def delete_note(note_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM study_notes WHERE id = ?",(note_id,))
    connection.commit()
    connection.close()
def update_note(note_id, title, subject, content):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE study_notes
        SET title = ?, subject = ?, content = ?
        WHERE id = ?
    """, (title, subject, content, note_id))
    connection.commit()
    connection.close()
def create_flashcards_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            subject TEXT
        )
    """)
    connection.commit()
    connection.close()
def add_flashcard(question, answer, subject):
    create_flashcards_table()
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO flashcards (question, answer, subject)
        VALUES (?, ?, ?)
    """, (question, answer, subject))
    connection.commit()
    connection.close()
def get_flashcards():
    create_flashcards_table()
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM flashcards ORDER BY id DESC")
    cards = cursor.fetchall()
    connection.close()
    return cards
def delete_flashcard(card_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM flashcards WHERE id = ?",(card_id,))
    connection.commit()
    connection.close()
def save_quiz_result(score, total):
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    percentage = (score / total * 100) if total > 0 else 0
    cursor.execute("""
        INSERT INTO quiz_results (score, total, percentage)
        VALUES (?, ?, ?)
    """, (score, total, percentage))
    connection.commit()
    connection.close()
def get_quiz_results():
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        SELECT * FROM quiz_results
        ORDER BY id DESC
    """)
    results = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return results
def save_quiz_result(score, total):
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    percentage = round(score / total * 100, 2) if total > 0 else 0
    cursor.execute("""
        INSERT INTO quiz_results (score, total, percentage)
        VALUES (?, ?, ?)
    """, (score, total, percentage))
    connection.commit()
    connection.close()
def get_quiz_results():
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        SELECT id, score, total, percentage, created_at
        FROM quiz_results
        ORDER BY id DESC
    """)
    results = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return results
def save_study_goal(weekly_goal, hours_studied):
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY,
            weekly_goal REAL NOT NULL,
            hours_studied REAL NOT NULL
        )
    """)
    cursor.execute("""
        INSERT OR REPLACE INTO study_goals
        (id, weekly_goal, hours_studied)
        VALUES (1, ?, ?)
    """, (weekly_goal, hours_studied))
    connection.commit()
    connection.close()
def get_study_goal():
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY,
            weekly_goal REAL NOT NULL,
            hours_studied REAL NOT NULL
        )
    """)
    cursor.execute("""
        SELECT weekly_goal, hours_studied
        FROM study_goals
        WHERE id = 1
    """)
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return dict(row)
def create_users_table():
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    connection.commit()
    connection.close()
def register_user(username, password):
    import sqlite3
    import hashlib
    import secrets
    username = username.strip()
    if not username or len(password) < 8:
        return False, "Username is required and password must have at least 8 characters"
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()
    stored_hash = salt + "$" + password_hash
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    try:
        cursor.execute("""INSERT INTO users(username, password_hash) VALUES(?, ?)""", (username, stored_hash))
        connection.commit()
        return True, " Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "This username already exists"
    finally:
        connection.close()
def verify_user(username, password):
    import sqlite3
    import hashlib
    import hmac
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute( "SELECT password_hash FROM users WHERE username = ?", (username.strip(),))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return False
    try:
        salt, saved_hash = row[0].split("$", 1)
        calculated_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200000).hex()
        return hmac.compare_digest(calculated_hash, saved_hash)
    except(ValueError, TypeError):
        return False
def get_user_id(username):
    import sqlite3
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?",(username.strip(),))
    row = cursor.fetchone()
    connection.close()
    return row[0] if row else None
def add_user_id_columns():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    tables = [
        "study_tasks",
        "study_notes",
        "flashcards",
        "quiz_results",
        "study_goals"
    ]
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if columns and "user_id" not in columns:
            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN user_id INTEGER"
            )
    connection.commit()
    connection.close()
def assign_existing_data_to_user():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    tables = [
        "study_tasks",
        "study_notes",
        "flashcards",
        "quiz_results",
        "study_goals"
    ]
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if columns and "user_id" in columns:
            cursor.execute(f"UPDATE {table} SET user_id = 1 WHERE user_id IS NULL")
    connection.commit()
    connection.close()
def migrate_user_data():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()
    tables = [
        "study_tasks",
        "study_notes",
        "flashcards",
        "quiz_results",
        "study_goals"
    ]
    try:
        for table in tables:
            cursor.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name=?",
                (table,)
            )
            if cursor.fetchone() is None:
                continue
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            if "user_id" not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN user_id INTEGER")
            cursor.execute(f"UPDATE {table} SET user_id = ? ""WHERE user_id IS NULL",(1,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
if __name__ == "_main_":
    create_database()
    fix_database()
    create_notes_table()
    create_flashcards_table()
    create_users_table()
    migrate_user_data()
    print("StudyBuddy AI database migration completed!")