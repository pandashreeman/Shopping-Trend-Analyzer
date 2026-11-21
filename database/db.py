
import sqlite3
import hashlib
import secrets
import hmac
import pandas as pd

DATABASE = "shopping_trend.db"


# Connect to database
def get_connection():
    return sqlite3.connect(DATABASE)


# Create users table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)


    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            customer_id TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            purchase_amount REAL NOT NULL,
            payment_method TEXT,
            purchase_date TEXT NOT NULL
        )
    """)

    # Analysis History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analysis_type TEXT NOT NULL,
            result_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# Hash password
def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_hex(16)

    hashed_password = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        bytes.fromhex(salt),
        100000
    )

    return hashed_password.hex(), salt


# Register new user
def register_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password, salt = hash_password(password)

    try:
        cursor.execute("""
            INSERT INTO users (username, email, password, salt)
            VALUES (?, ?, ?, ?)
        """, (username, email, hashed_password, salt))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# Login user
def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password, salt FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, username, stored_password, salt = user

        hashed_password, _ = hash_password(password, salt)

        if hmac.compare_digest(hashed_password, stored_password):
            return {
                "id": user_id,
                "username": username,
                "email": email
            }

    return None

# Add a new shopping transaction
def add_transaction(data):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO transactions (
                transaction_id,
                customer_id,
                customer_name,
                age,
                gender,
                product,
                category,
                quantity,
                purchase_amount,
                payment_method,
                purchase_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# Get all shopping transactions
def get_transactions():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM transactions ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


# Search transaction by ID
def search_transaction(transaction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE transaction_id = ?
    """, (transaction_id,))

    result = cursor.fetchone()

    conn.close()

    return result

# Update an existing transaction
def update_transaction(transaction_id, data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET customer_id = ?,
            customer_name = ?,
            age = ?,
            gender = ?,
            product = ?,
            category = ?,
            quantity = ?,
            purchase_amount = ?,
            payment_method = ?,
            purchase_date = ?
        WHERE transaction_id = ?
    """, data + (transaction_id,))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# Delete a transaction
def delete_transaction(transaction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE transaction_id = ?
    """, (transaction_id,))

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted

# Save Analysis History
def save_analysis(user_id, analysis_type, result_data):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            user_id, analysis_type, result_data
        )
        VALUES (?, ?, ?)
    """, (user_id, analysis_type, result_data))

    conn.commit()
    conn.close()


# Get Analysis History
def get_analysis_history(user_id):

    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT id, analysis_type, result_data, created_at
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, conn, params=(user_id,))

    conn.close()

    return df