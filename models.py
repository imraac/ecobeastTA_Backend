from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class SafariPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.String(100))
    location = db.Column(db.String(200))
    image_urls = db.Column(db.Text) 
    rating = db.Column(db.Float)
    reviews = db.Column(db.Integer)
    description = db.Column(db.Text)
    route_map = db.Column(db.String(300))
    overview = db.Column(db.Text)
    day_by_day = db.Column(db.Text)
    rates = db.Column(db.Text)
    inclusions = db.Column(db.Text)
    getting_there = db.Column(db.Text)
    offered_by = db.Column(db.String(200))
    
    tour_features = db.Column(db.Text)   
    route_details = db.Column(db.Text)
    route_points = db.Column(db.Text)    
    is_archived = db.Column(db.Boolean, default=False, nullable=False)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)  # Store hashed password
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())

    @validates('email')
    def validate_email(self, key, email):
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": str(self.created_at),
        }