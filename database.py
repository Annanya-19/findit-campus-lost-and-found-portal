
import sqlite3
import os

# Database location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DATABASE = os.path.join(INSTANCE_DIR, "findit.db")


# Connect to database
def get_db_connection():

    os.makedirs(INSTANCE_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    # Enable foreign key relationships
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


# Create all database tables
def create_tables():

    conn = get_db_connection()
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
    conn.close()

    print("================================")
    print("FindIt Database Created!")
    print("Users Table Created!")
    print("Items Table Created!")
    print("Claims Table Created!")
    print("================================")


# Run database creation
if __name__ == "__main__":
    create_tables()
