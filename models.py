from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SafariPackage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price_range = db.Column(db.String(100))
    location = db.Column(db.String(200))
    image_url = db.Column(db.String(300))
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
    
    # Store lists as JSON strings
    tour_features = db.Column(db.Text)     # Expected to store JSON list (e.g. ["Private tour", ...])
    route_details = db.Column(db.Text)
    route_points = db.Column(db.Text)      # New field: stores JSON list like ["Day 1: Nairobi", "Day 2: ..."]
