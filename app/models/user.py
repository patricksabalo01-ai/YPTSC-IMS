from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
# USER MODEL
class User(db.Model):
    __tablename__ = "users"
    # PRIMARY KEY
    id = db.Column(db.Integer, primary_key=True)
    # USER INFORMATION
    full_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # PASSWORD
    password_hash = db.Column(db.String(255), nullable=False)
    # USER ACCESS
    role = db.Column(db.String(50), nullable=False, default="Staff")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    # TIMESTAMPS
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # PASSWORD METHODS
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
