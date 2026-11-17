"""Login, user creation, password hashing, and password changes."""
import hashlib
import hmac
import secrets
from config import USERS_FILE
from storage import read_records, write_records, append_record
from interface import ask, message

USER_FIELDS = ["username", "role", "salt", "password_hash"]
ITERATIONS = 200_000

def hash_password(password, salt=None):
    """Hash a password with a random salt using PBKDF2-HMAC-SHA256."""
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 bytes.fromhex(salt), ITERATIONS).hex()
    return salt, digest

def verify_password(password, salt, saved_hash):
    """Safely compare a password with its stored salted hash."""
    _, candidate = hash_password(password, salt)
    return hmac.compare_digest(candidate, saved_hash)

def load_users():
    """Load all registered user accounts."""
    return read_records(USERS_FILE, USER_FIELDS)

def seed_demo_users():
    """Create demo administrator and staff accounts if the user file is empty."""
    users = load_users()
    if users:
        return
    demo = []
    for username, role, password in [
        ("admin", "Administrator", "Admin@123"),
        ("staff", "Staff", "Staff@123")
    ]:
        salt, digest = hash_password(password)
        demo.append({"username": username, "role": role, "salt": salt,
                     "password_hash": digest})
    write_records(USERS_FILE, USER_FIELDS, demo)

def login():
    """Ask for credentials and return the authenticated user or None."""
    message("Enter your account credentials.")
    username = ask("Username: ")
    password = ask("Password: ")
    for user in load_users():
        if user["username"].lower() == username.lower() and verify_password(
                password, user["salt"], user["password_hash"]):
            message(f"Login successful. Welcome, {user['username']}!", "success")
            return user
    message("Invalid username or password.", "error")
    return None

def add_user():
    """Allow an administrator to create a staff or administrator account."""
    users = load_users()
    username = ask("New username: ")
    if any(u["username"].lower() == username.lower() for u in users):
        message("That username already exists.", "error")
        return
    role_choice = ask("Role (1=Administrator, 2=Staff): ")
    if role_choice not in ("1", "2"):
        message("Invalid role.", "error")
        return
    password = ask("Temporary password (minimum 8 characters): ")
    if len(password) < 8:
        message("Password must contain at least 8 characters.", "error")
        return
    salt, digest = hash_password(password)
    users.append({"username": username,
                  "role": "Administrator" if role_choice == "1" else "Staff",
                  "salt": salt, "password_hash": digest})
    if write_records(USERS_FILE, USER_FIELDS, users):
        message("User account created.", "success")

def change_password(user):
    """Verify the current password before saving a new salted password hash."""
    current = ask("Current password: ")
    if not verify_password(current, user["salt"], user["password_hash"]):
        message("Current password is incorrect.", "error")
        return
    new_password = ask("New password (minimum 8 characters): ")
    if len(new_password) < 8:
        message("Password must contain at least 8 characters.", "error")
        return
    confirm = ask("Confirm new password: ")
    if new_password != confirm:
        message("Passwords do not match.", "error")
        return
    salt, digest = hash_password(new_password)
    users = load_users()
    for record in users:
        if record["username"] == user["username"]:
            record["salt"], record["password_hash"] = salt, digest
            user["salt"], user["password_hash"] = salt, digest
    if write_records(USERS_FILE, USER_FIELDS, users):
        message("Password updated successfully.", "success")
