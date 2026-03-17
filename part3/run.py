from app import create_app
from app.services import facade  # <- use the shared singleton
from flask_cors import CORS
from flask import request  # needed for the before_request hook

app = create_app()

# Configuration of CORS to allow frontend origin and handle credentials
CORS(app, origins=["http://127.0.0.1:5500"], supports_credentials=True)

# Bypass authentication for OPTIONS requests (preflight)
@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        return '', 200  # Let Flask-CORS add the headers

# --- Create admin user only if it doesn't exist ---
admin_email = "admin@mail.com"
admin_password = "admin123"

existing_admin = facade.get_user_by_email(admin_email)

if not existing_admin:
    admin = facade.create_user({
        "first_name": "Admin",
        "last_name": "User",
        "email": admin_email,
        "password": admin_password,
        "is_admin": True
    })
    print("ADMIN CREATED:", admin_email)
    print("HASHED PASSWORD:", admin.password)
else:
    print("Admin already exists:", admin_email)
    admin = existing_admin
    print("HASHED PASSWORD:", admin.password)

# --- Start Flask server ---
if __name__ == "__main__":
    app.run(debug=True)
