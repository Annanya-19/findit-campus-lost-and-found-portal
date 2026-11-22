
import os
import re
import sqlite3
import uuid
from datetime import datetime

from flask import (
    Flask, request, jsonify, session,
    render_template, url_for, redirect
)
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db_connection, create_tables


# ==========================================
# CONFIGURATION
# ==========================================

ADMIN_EMAIL = "admin@findit.com"
ADMIN_PASSWORD = "FindItAdmin@123"

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# Demo-only settings. Change before any public deployment.
app.config["SECRET_KEY"] = "findit-development-secret-change-later"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

CORS(app, supports_credentials=True)

create_tables()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_request_data():
    return request.get_json(silent=True) or request.form.to_dict()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def student_required():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please log in first."
        }), 401

    if session.get("role") != "student":
        return jsonify({
            "success": False,
            "message": "Student access required."
        }), 403

    return None


def admin_required():
    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please log in first."
        }), 401

    if session.get("role") != "admin":
        return jsonify({
            "success": False,
            "message": "Admin access required."
        }), 403

    return None


def item_image_url(image):
    if image:
        return url_for("static", filename=f"uploads/{image}")
    return None


# ==========================================
# HOME
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("index.html")


# ==========================================
# STUDENT REGISTRATION
# ==========================================

@app.route("/api/register", methods=["POST"])
def register_api():

    data = get_request_data()

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    phone_number = data.get("phone_number", "").strip()
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    terms_accepted = data.get("terms_accepted")

    if not all([full_name, email, phone_number, password]):
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields."
        }), 400

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return jsonify({
            "success": False,
            "message": "Enter a valid email address."
        }), 400

    if not re.fullmatch(r"[0-9]{10}", phone_number):
        return jsonify({
            "success": False,
            "message": "Enter a valid 10-digit phone number."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    if password != confirm_password:
        return jsonify({
            "success": False,
            "message": "Passwords do not match."
        }), 400

    if str(terms_accepted).lower() not in ("1", "true", "on", "yes"):
        return jsonify({
            "success": False,
            "message": "Please accept the campus guidelines."
        }), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()

    try:
        cursor = conn.execute("""
            INSERT INTO users
            (full_name, email, phone_number, password, terms_accepted)
            VALUES (?, ?, ?, ?, ?)
        """, (
            full_name,
            email,
            phone_number,
            hashed_password,
            1
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Registration successful!",
            "user_id": cursor.lastrowid
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    except Exception:
        app.logger.exception("Registration error")
        return jsonify({
            "success": False,
            "message": "Registration failed."
        }), 500

    finally:
        conn.close()


# ==========================================
# STUDENT / ADMIN LOGIN
# ==========================================

@app.route("/api/login", methods=["POST"])
def login_api():

    data = get_request_data()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    role = data.get("role", "student").strip().lower()

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    # ADMIN LOGIN
    if role == "admin":

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:

            session.clear()
            session["user_id"] = 0
            session["full_name"] = "FindIt Admin"
            session["email"] = ADMIN_EMAIL
            session["role"] = "admin"

            return jsonify({
                "success": True,
                "message": "Admin login successful!"
            }), 200

        return jsonify({
            "success": False,
            "message": "Invalid admin credentials."
        }), 401

    # STUDENT LOGIN
    if role != "student":
        return jsonify({
            "success": False,
            "message": "Invalid account type."
        }), 400

    conn = get_db_connection()

    try:
        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    finally:
        conn.close()

    if (
        user
        and user["role"] == "student"
        and check_password_hash(user["password"], password)
    ):

        session.clear()
        session["user_id"] = user["user_id"]
        session["full_name"] = user["full_name"]
        session["email"] = user["email"]
        session["role"] = "student"

        return jsonify({
            "success": True,
            "message": "Login successful!",
            "user": {
                "user_id": user["user_id"],
                "full_name": user["full_name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    return jsonify({
        "success": False,
        "message": "Invalid email or password."
    }), 401


# ==========================================
# LOGOUT
# ==========================================

@app.route("/api/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully."
    }), 200


# ==========================================
# CURRENT LOGGED-IN USER
# ==========================================

@app.route("/api/me", methods=["GET"])
def current_user():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please log in first."
        }), 401

    return jsonify({
        "success": True,
        "user": {
            "user_id": session["user_id"],
            "full_name": session["full_name"],
            "email": session["email"],
            "role": session["role"]
        }
    }), 200


# ==========================================
# REPORT LOST / FOUND ITEM
# ==========================================

@app.route("/api/items", methods=["POST"])
def report_item_api():

    auth_error = student_required()
    if auth_error:
        return auth_error

    item_name = request.form.get("item_name", "").strip()
    item_description = request.form.get("item_description", "").strip()
    category = request.form.get("category", "").strip()
    item_type = request.form.get("item_type", "").strip()
    location = request.form.get("location", "").strip()
    date_lost_found = request.form.get("date_lost_found", "").strip()

    if not all([item_name, category, item_type, location, date_lost_found]):
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields."
        }), 400

    if item_type not in ["Lost", "Found"]:
        return jsonify({
            "success": False,
            "message": "Item type must be Lost or Found."
        }), 400

    try:
        datetime.strptime(date_lost_found, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid date format. Use YYYY-MM-DD."
        }), 400

    image = request.files.get("image")
    image_filename = None

    if image and image.filename:

        if not allowed_file(image.filename):
            return jsonify({
                "success": False,
                "message": "Invalid image format."
            }), 400

        extension = secure_filename(image.filename).rsplit(".", 1)[1].lower()
        image_filename = f"{uuid.uuid4().hex}.{extension}"

        image.save(os.path.join(
            app.config["UPLOAD_FOLDER"],
            image_filename
        ))

    conn = get_db_connection()

    try:
        cursor = conn.execute("""
            INSERT INTO items
            (user_id, item_name, item_description, category,
             item_type, location, date_lost_found, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            item_name,
            item_description,
            category,
            item_type,
            location,
            date_lost_found,
            image_filename
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": f"{item_type} item reported successfully!",
            "item_id": cursor.lastrowid,
            "image": image_filename
        }), 201

    except Exception:
        app.logger.exception("Item reporting failed")
        return jsonify({
            "success": False,
            "message": "Unable to report item."
        }), 500

    finally:
        conn.close()


# ==========================================
# BROWSE / SEARCH ITEMS
# ==========================================

@app.route("/api/items", methods=["GET"])
def get_items():

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    item_type = request.args.get("item_type", "").strip()

    conn = get_db_connection()

    try:
        query = """
            SELECT items.*, users.full_name AS reporter_name
            FROM items
            JOIN users ON items.user_id = users.user_id
            WHERE 1=1
        """

        params = []

        if search:
            query += """
                AND (
                    items.item_name LIKE ?
                    OR items.location LIKE ?
                    OR items.item_description LIKE ?
                )
            """
            value = f"%{search}%"
            params.extend([value, value, value])

        if category:
            query += " AND items.category = ?"
            params.append(category)

        if item_type:
            if item_type not in ["Lost", "Found"]:
                return jsonify({
                    "success": False,
                    "message": "Invalid item type."
                }), 400

            query += " AND items.item_type = ?"
            params.append(item_type)

        query += " ORDER BY items.created_at DESC"

        items = conn.execute(query, params).fetchall()

        result = []

        for item in items:
            item_data = dict(item)
            item_data["image_url"] = item_image_url(item_data["image"])
            result.append(item_data)

        return jsonify({
            "success": True,
            "count": len(result),
            "items": result
        }), 200

    finally:
        conn.close()


# ==========================================
# SUBMIT A CLAIM
# ==========================================

@app.route("/api/claims", methods=["POST"])
def submit_claim():

    auth_error = student_required()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    item_id = data.get("item_id")
    claim_message = (data.get("claim_message") or "").strip()

    if not item_id or not claim_message:
        return jsonify({
            "success": False,
            "message": "Item ID and claim message are required."
        }), 400

    conn = get_db_connection()

    try:
        item = conn.execute("""
            SELECT user_id, status
            FROM items
            WHERE item_id = ?
        """, (item_id,)).fetchone()

        if item is None:
            return jsonify({
                "success": False,
                "message": "Item not found."
            }), 404

        if item["status"] != "Active":
            return jsonify({
                "success": False,
                "message": "This item is no longer active."
            }), 400

        if item["user_id"] == session["user_id"]:
            return jsonify({
                "success": False,
                "message": "You cannot claim an item reported by yourself."
            }), 403

        conn.execute("""
            INSERT INTO claims
            (item_id, claimant_id, claim_message)
            VALUES (?, ?, ?)
        """, (item_id, session["user_id"], claim_message))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Claim submitted successfully!"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "You have already claimed this item or the item does not exist."
        }), 409

    finally:
        conn.close()


# ==========================================
# VIEW MY CLAIMS
# ==========================================

@app.route("/api/claims", methods=["GET"])
def get_claims():

    auth_error = student_required()
    if auth_error:
        return auth_error

    conn = get_db_connection()

    try:
        claims = conn.execute("""
            SELECT
                claims.claim_id,
                claims.item_id,
                claims.claim_message,
                claims.claim_status,
                claims.created_at,
                items.item_name,
                items.category,
                items.item_type,
                items.date_lost_found,
                items.location,
                items.image
            FROM claims
            JOIN items ON claims.item_id = items.item_id
            WHERE claims.claimant_id = ?
            ORDER BY claims.created_at DESC
        """, (session["user_id"],)).fetchall()

        result = []

        for claim in claims:
            claim_data = dict(claim)
            claim_data["image_url"] = item_image_url(claim_data["image"])
            result.append(claim_data)

        return jsonify({
            "success": True,
            "count": len(result),
            "claims": result
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: DASHBOARD STATISTICS
# ==========================================

@app.route("/api/admin/stats", methods=["GET"])
def admin_stats_api():

    auth_error = admin_required()
    if auth_error:
        return auth_error

    conn = get_db_connection()

    try:
        total_reports = conn.execute(
            "SELECT COUNT(*) FROM items"
        ).fetchone()[0]

        active_lost_items = conn.execute("""
            SELECT COUNT(*) FROM items
            WHERE item_type = 'Lost' AND status = 'Active'
        """).fetchone()[0]

        found_in_custody = conn.execute("""
            SELECT COUNT(*) FROM items
            WHERE item_type = 'Found' AND status = 'Active'
        """).fetchone()[0]

        pending_claims = conn.execute("""
            SELECT COUNT(*) FROM claims
            WHERE claim_status = 'Pending'
        """).fetchone()[0]

        return jsonify({
            "success": True,
            "total_reports": total_reports,
            "active_lost_items": active_lost_items,
            "found_in_custody": found_in_custody,
            "pending_claims": pending_claims
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: VIEW ALL REPORTED ITEMS
# ==========================================

@app.route("/api/admin/items", methods=["GET"])
def admin_get_items():

    auth_error = admin_required()
    if auth_error:
        return auth_error

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    conn = get_db_connection()

    try:
        query = """
            SELECT
                items.*,
                users.full_name AS reporter_name,
                users.email AS reporter_email
            FROM items
            JOIN users ON items.user_id = users.user_id
            WHERE 1=1
        """

        params = []

        if search:
            query += """
                AND (
                    items.item_name LIKE ?
                    OR items.location LIKE ?
                    OR users.full_name LIKE ?
                )
            """
            value = f"%{search}%"
            params.extend([value, value, value])

        if category:
            query += " AND items.category = ?"
            params.append(category)

        query += " ORDER BY items.created_at DESC"

        items = conn.execute(query, params).fetchall()

        result = []

        for item in items:
            item_data = dict(item)
            item_data["image_url"] = item_image_url(item_data["image"])
            result.append(item_data)

        return jsonify({
            "success": True,
            "count": len(result),
            "items": result
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: VIEW PENDING CLAIMS
# ==========================================

@app.route("/api/admin/claims", methods=["GET"])
def admin_get_claims():

    auth_error = admin_required()
    if auth_error:
        return auth_error

    conn = get_db_connection()

    try:
        claims = conn.execute("""
            SELECT
                claims.claim_id,
                claims.item_id,
                claims.claim_message,
                claims.claim_status,
                claims.created_at,
                items.item_name,
                items.item_type,
                items.category,
                users.full_name AS claimant_name,
                users.email AS claimant_email,
                users.phone_number AS claimant_phone
            FROM claims
            JOIN items ON claims.item_id = items.item_id
            JOIN users ON claims.claimant_id = users.user_id
            WHERE claims.claim_status = 'Pending'
            ORDER BY claims.created_at DESC
        """).fetchall()

        result = [dict(claim) for claim in claims]

        return jsonify({
            "success": True,
            "count": len(result),
            "claims": result
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: APPROVE / REJECT CLAIM
# ==========================================

@app.route("/api/admin/claims/<int:claim_id>/decision", methods=["POST"])
def admin_claim_decision(claim_id):

    auth_error = admin_required()
    if auth_error:
        return auth_error

    data = request.get_json(silent=True) or {}
    decision = data.get("decision", "").strip().lower()

    if decision not in ["approved", "rejected"]:
        return jsonify({
            "success": False,
            "message": "Decision must be approved or rejected."
        }), 400

    new_status = "Approved" if decision == "approved" else "Rejected"

    conn = get_db_connection()

    try:
        claim = conn.execute("""
            SELECT claim_id, item_id, claim_status
            FROM claims
            WHERE claim_id = ?
        """, (claim_id,)).fetchone()

        if claim is None:
            return jsonify({
                "success": False,
                "message": "Claim not found."
            }), 404

        if claim["claim_status"] != "Pending":
            return jsonify({
                "success": False,
                "message": "This claim has already been processed."
            }), 409

        conn.execute("""
            UPDATE claims
            SET claim_status = ?
            WHERE claim_id = ?
        """, (new_status, claim_id))

        # If approved, mark the item as resolved.
        if new_status == "Approved":
            conn.execute("""
                UPDATE items
                SET status = 'Resolved'
                WHERE item_id = ?
            """, (claim["item_id"],))

        conn.commit()

        return jsonify({
            "success": True,
            "message": f"Claim {decision} successfully.",
            "claim_status": new_status
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: MARK ITEM AS RESOLVED
# ==========================================

@app.route("/api/admin/items/<int:item_id>/resolve", methods=["POST"])
def admin_resolve_item(item_id):

    auth_error = admin_required()
    if auth_error:
        return auth_error

    conn = get_db_connection()

    try:
        item = conn.execute("""
            SELECT item_id
            FROM items
            WHERE item_id = ?
        """, (item_id,)).fetchone()

        if item is None:
            return jsonify({
                "success": False,
                "message": "Item not found."
            }), 404

        conn.execute("""
            UPDATE items
            SET status = 'Resolved'
            WHERE item_id = ?
        """, (item_id,))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Item marked as resolved."
        }), 200

    finally:
        conn.close()


# ==========================================
# ADMIN: DELETE REPORTED ITEM
# ==========================================

@app.route("/api/admin/items/<int:item_id>", methods=["DELETE"])
def admin_delete_item(item_id):

    auth_error = admin_required()
    if auth_error:
        return auth_error

    conn = get_db_connection()

    try:
        item = conn.execute("""
            SELECT image
            FROM items
            WHERE item_id = ?
        """, (item_id,)).fetchone()

        if item is None:
            return jsonify({
                "success": False,
                "message": "Item not found."
            }), 404

        # Delete associated claims first.
        conn.execute("""
            DELETE FROM claims
            WHERE item_id = ?
        """, (item_id,))

        conn.execute("""
            DELETE FROM items
            WHERE item_id = ?
        """, (item_id,))

        conn.commit()

        # Remove uploaded image if it exists.
        if item["image"]:
            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                item["image"]
            )

            if os.path.isfile(image_path):
                os.remove(image_path)

        return jsonify({
            "success": True,
            "message": "Item deleted successfully."
        }), 200

    finally:
        conn.close()


# ==========================================
# FRONTEND PAGE ROUTES
# ==========================================

@app.route("/browse")
def browse():
    return render_template("browse.html")


@app.route("/report-item")
def report_item_page():
    return render_template("report-item.html")


@app.route("/my-claims")
def my_claims():
    return render_template("my-claims.html")


@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if session.get("role") != "admin":
        return "Access Denied: Admins Only", 403

    return render_template("admin-dashboard.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/item-details")
def item_details():
    item_id = request.args.get("id")
    return render_template("item-details.html", item_id=item_id)


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True, port=5000)
