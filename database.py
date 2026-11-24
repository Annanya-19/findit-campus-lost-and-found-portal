
import sqlite3
import os

# Use Railway's persistent volume when available.
# Otherwise, use the local instance folder.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = (
    os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
    or os.environ.get("DATA_DIR")
    or os.path.join(BASE_DIR, "instance")
)

DATABASE = os.path.join(DATA_DIR, "findit.db")


def get_db_connection():
    os.makedirs(DATA_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def create_tables():
    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        # 1. USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number TEXT NOT NULL,
                password TEXT NOT NULL,
                terms_accepted INTEGER NOT NULL DEFAULT 0,
                role TEXT NOT NULL DEFAULT 'student'
                    CHECK(role IN ('student', 'admin')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 2. ITEMS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_name TEXT NOT NULL,
                item_description TEXT,
                category TEXT NOT NULL,
                item_type TEXT NOT NULL
                    CHECK(item_type IN ('Lost', 'Found')),
                location TEXT NOT NULL,
                date_lost_found DATE NOT NULL,
                image TEXT,
                status TEXT NOT NULL DEFAULT 'Active'
                    CHECK(status IN ('Active', 'Resolved')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
            )
        """)

        # 3. CLAIMS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                claimant_id INTEGER NOT NULL,
                claim_message TEXT NOT NULL,
                claim_status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK(claim_status IN
                    ('Pending', 'Approved', 'Rejected')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(item_id)
                    REFERENCES items(item_id),
                FOREIGN KEY(claimant_id)
                    REFERENCES users(user_id),
                UNIQUE(item_id, claimant_id)
            )
        """)

        conn.commit()

        print("FindIt Database Created!")
        print("Users, Items and Claims tables ready!")

    finally:
        conn.close()


if __name__ == "__main__":
    create_tables()
