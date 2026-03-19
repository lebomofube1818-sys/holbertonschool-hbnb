from app import db
from .base_model import BaseModel
import uuid
import re
from datetime import datetime
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):

    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = db.relationship('Place', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    all_users = {}   # in-memory storage

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if not first_name or len(first_name) > 50:
            raise ValueError("first_name is required and must be <= 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")
        if not email or not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = bool(is_admin)

        # Hash and store the password on instantiation
        self.hash_password(password)

        # store user in memory
        User.all_users[self.id] = self

    def _is_valid_email(self, email):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if key == "password":
                self.hash_password(value)
            elif hasattr(self, key):
                setattr(self, key, value)
        self.save()
