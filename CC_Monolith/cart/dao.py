import json
import os.path
import sqlite3


def connect(path='carts.db'):
    """
    Establishes a database connection and creates tables if they do not exist.
    """
    exists = os.path.exists(path)
    conn = sqlite3.connect(path, check_same_thread=False)
    if not exists:
        create_tables(conn)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables(conn):
    """
    Creates the necessary tables in the database.
    """
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT DEFAULT '[]',
            cost REAL DEFAULT 0
        )
    ''')
    conn.commit()


def get_cart(username, path='carts.db'):
    """
    Retrieves the cart contents for the given username.
    """
    conn = connect(path)
    try:
        cursor = conn.cursor()
        query = "SELECT contents FROM carts WHERE username = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and result['contents']:
            try:
                return json.loads(result['contents'])
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in 'contents' for username: {username}")
                return []
        print(f"DEBUG: No cart contents found for {username}")
        return []
    except sqlite3.Error as e:
        print(f"Database error in get_cart: {e}")
        conn.close()
        return []


def add_to_cart(username, product_id, path='carts.db'):
    """
    Adds a product to the user's cart.
    """
    conn = connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
        result = cursor.fetchone()
        contents = json.loads(result['contents']) if result else []
        contents.append(product_id)
        cursor.execute(
            'INSERT OR REPLACE INTO carts (username, contents) VALUES (?, ?)', 
            (username, json.dumps(contents))
        )
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error in add_to_cart: {e}")
        conn.close()


def remove_from_cart(username, product_id, path='carts.db'):
    """
    Removes a product from the user's cart.
    """
    conn = connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
        result = cursor.fetchone()
        if not result:
            print(f"DEBUG: No cart found for {username} to remove product {product_id}")
            cursor.close()
            conn.close()
            return
        contents = json.loads(result['contents'])
        if product_id in contents:
            contents.remove(product_id)
            cursor.execute(
                'INSERT OR REPLACE INTO carts (username, contents) VALUES (?, ?)', 
                (username, json.dumps(contents))
            )
            conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error in remove_from_cart: {e}")
        conn.close()


def delete_cart(username, path='carts.db'):
    """
    Deletes the cart for the given username.
    """
    conn = connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error in delete_cart: {e}")
        conn.close()

