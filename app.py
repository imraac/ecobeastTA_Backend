# # from flask import Flask, request, redirect, url_for, jsonify
# # from flask_cors import CORS
# # import requests
# # import json
# # import os

# # app = Flask(__name__)
# # CORS(app)  # Enable CORS

# # app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# # # PayPal credentials
# # PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
# # PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
# # PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"

# # def get_paypal_access_token():
# #     auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
# #     headers = {
# #         'Accept': 'application/json',
# #         'Accept-Language': 'en_US',
# #         'Content-Type': 'application/x-www-form-urlencoded'
# #     }
# #     response = requests.post(f"{PAYPAL_API_BASE}/v1/oauth2/token",
# #                              auth=auth,
# #                              headers=headers,
# #                              data={'grant_type': 'client_credentials'})
# #     response.raise_for_status()
# #     return response.json()['access_token']

# # @app.route('/create-payment', methods=['POST'])
# # def create_payment():
# #     access_token = get_paypal_access_token()
# #     headers = {
# #         'Content-Type': 'application/json',
# #         'Authorization': f'Bearer {access_token}'
# #     }
# #     payment_data = {
# #         "intent": "AUTHORIZE",
# #         "payer": {
# #             "payment_method": "paypal"
# #         },
# #         "transactions": [{
# #             "amount": {
# #                 "total": "10.00",
# #                 "currency": "USD"
# #             },
# #             "description": "Subscription payment"
# #         }],
# #         "redirect_urls": {
# #             "return_url": url_for('execute_payment', _external=True),
# #             "cancel_url": url_for('cancel', _external=True)
# #         }
# #     }
# #     response = requests.post(f"{PAYPAL_API_BASE}/v1/payments/payment",
# #                              headers=headers,
# #                              data=json.dumps(payment_data))
# #     response.raise_for_status()
# #     payment = response.json()
# #     approval_url = next(link['href'] for link in payment['links'] if link['rel'] == 'approval_url')
    
# #     return jsonify({"success": True, "approvalUrl": approval_url})

# # @app.route('/execute-payment')
# # def execute_payment():
# #     payment_id = request.args.get('paymentId')
# #     payer_id = request.args.get('PayerID')

# #     access_token = get_paypal_access_token()
# #     headers = {
# #         'Content-Type': 'application/json',
# #         'Authorization': f'Bearer {access_token}'
# #     }
# #     execute_data = {
# #         "payer_id": payer_id
# #     }
# #     url = f"{PAYPAL_API_BASE}/v1/payments/payment/{payment_id}/execute"
# #     response = requests.post(url, headers=headers, data=json.dumps(execute_data))

# #     if response.status_code == 200:
# #         payment = response.json()
# #         if payment['state'] == 'approved':
# #             return jsonify({"success": True, "message": "Your subscription was successful!"})
# #         return jsonify({"success": False, "message": "Payment was not approved."})
# #     else:
# #         return jsonify({"success": False, "message": "Payment execution failed."})

# # @app.route('/cancel')
# # def cancel():
# #     return jsonify({"success": False, "message": "Your subscription was canceled."})

# # if __name__ == '__main__':
# #     app.run(debug=True)




# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from flask_migrate import Migrate
# import os
# import json

# # Configuration
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Initialize app
# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# CORS(app)

# # SafariPackage model
# class SafariPackage(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     price_range = db.Column(db.String(100))
#     location = db.Column(db.String(200))
#     image_url = db.Column(db.String(300))
#     rating = db.Column(db.Float)
#     reviews = db.Column(db.Integer)
#     description = db.Column(db.Text)
#     route_map = db.Column(db.String(300))

#     overview = db.Column(db.Text)
#     day_by_day = db.Column(db.Text)
#     rates = db.Column(db.Text)
#     inclusions = db.Column(db.Text)
#     getting_there = db.Column(db.Text)
#     offered_by = db.Column(db.String(200))
#     tour_features = db.Column(db.Text)    # Stored as JSON string
#     route_details = db.Column(db.Text)
#     route_points = db.Column(db.Text)     # Stored as JSON string

# # Helper to safely parse JSON fields
# def safe_json_parse(raw):
#     try:
#         return json.loads(raw) if raw and raw.strip() else []
#     except json.JSONDecodeError:
#         return []

# # GET all safari packages
# @app.route("/api/safaris", methods=["GET"])
# def get_safaris():
#     safaris = SafariPackage.query.all()
#     return jsonify([{
#         "id": s.id,
#         "title": s.title,
#         "priceRange": s.price_range,
#         "location": s.location,
#         "imageUrl": s.image_url,
#         "rating": s.rating,
#         "reviews": s.reviews,
#         "description": s.description,
#         "routeMap": s.route_map,
#         "overview": s.overview,
#         "dayByDay": s.day_by_day,
#         "rates": s.rates,
#         "inclusions": s.inclusions,
#         "gettingThere": s.getting_there,
#         "offeredBy": s.offered_by,
#         "tourFeatures": safe_json_parse(s.tour_features),
#         "routeDetails": s.route_details,
#         "routePoints": safe_json_parse(s.route_points)
#     } for s in safaris])

# # GET safari package by ID
# @app.route("/api/safaris/<int:id>", methods=["GET"])
# def get_safari_by_id(id):
#     s = SafariPackage.query.get_or_404(id)
#     return jsonify({
#         "id": s.id,
#         "title": s.title,
#         "priceRange": s.price_range,
#         "location": s.location,
#         "imageUrl": s.image_url,
#         "rating": s.rating,
#         "reviews": s.reviews,
#         "description": s.description,
#         "routeMap": s.route_map,
#         "overview": s.overview,
#         "dayByDay": s.day_by_day,
#         "rates": s.rates,
#         "inclusions": s.inclusions,
#         "gettingThere": s.getting_there,
#         "offeredBy": s.offered_by,
#         "tourFeatures": safe_json_parse(s.tour_features),
#         "routeDetails": s.route_details,
#         "routePoints": safe_json_parse(s.route_points)
#     })

# # POST new safari package(s)
# @app.route("/api/safaris", methods=["POST"])
# def add_safari_or_safaris():
#     data = request.get_json()

#     if isinstance(data, dict):
#         safaris = [data]
#     elif isinstance(data, list):
#         safaris = data
#     else:
#         return jsonify({"error": "Invalid input format"}), 400

#     created = []
#     for item in safaris:
#         try:
#             tour_features = item.get("tour_features")
#             if isinstance(tour_features, list):
#                 tour_features = json.dumps(tour_features)

#             route_points = item.get("route_points")
#             if isinstance(route_points, list):
#                 route_points = json.dumps(route_points)

#             new_safari = SafariPackage(
#                 title=item["title"],
#                 price_range=item.get("price_range"),
#                 location=item.get("location"),
#                 image_url=item.get("image_url"),
#                 rating=item.get("rating"),
#                 reviews=item.get("reviews"),
#                 description=item.get("description"),
#                 route_map=item.get("route_map"),
#                 overview=item.get("overview"),
#                 day_by_day=item.get("day_by_day"),
#                 rates=item.get("rates"),
#                 inclusions=item.get("inclusions"),
#                 getting_there=item.get("getting_there"),
#                 offered_by=item.get("offered_by"),
#                 tour_features=tour_features,
#                 route_details=item.get("route_details"),
#                 route_points=route_points
#             )
#             db.session.add(new_safari)
#             created.append(new_safari)
#         except KeyError as e:
#             return jsonify({"error": f"Missing field: {e}"}), 400

#     db.session.commit()
#     return jsonify({"message": f"{len(created)} safari package(s) added successfully"}), 201

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from flask import Flask, jsonify, request ,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail, Message
from dotenv import load_dotenv

import json
import re
import os
from flask_restful import Api, Resource
import json
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import SafariPackage,User
from flask_bcrypt import Bcrypt

# Load environment variables
load_dotenv()

db_url = os.getenv("DATABASE_URL")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv() 
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Gmail SMTP
    MAIL_SERVER = 'smtp.zoho.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
 


# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app, resources={r"/api/*": {"origins": "https://ecobeastta-production.up.railway.app"}})

api = Api(app)

# SafariPackage model
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
    tour_features = db.Column(db.Text)
    route_details = db.Column(db.Text)
    route_points = db.Column(db.Text)
    is_archived = db.Column(db.Boolean, default=False, nullable=False)
# Helper to safely parse JSON fields
def safe_json_parse(raw):
    try:
        return json.loads(raw) if raw and raw.strip() else []
    except json.JSONDecodeError:
        return []
# GET all safari packages (including archived)
@app.route("/api/safaris", methods=["GET"])
def get_safaris():
    safaris = SafariPackage.query.all()  # no filter on is_archived
    return jsonify([{
        "id": s.id,
        "title": s.title,
        "priceRange": s.price_range,
        "location": s.location,
        "imageUrl": s.image_url,
        "rating": s.rating,
        "reviews": s.reviews,
        "description": s.description,
        "routeMap": s.route_map,
        "overview": s.overview,
        "dayByDay": s.day_by_day,
        "rates": s.rates,
        "inclusions": s.inclusions,
        "gettingThere": s.getting_there,
        "offeredBy": s.offered_by,
        "tourFeatures": safe_json_parse(s.tour_features),
        "routeDetails": s.route_details,
        "routePoints": safe_json_parse(s.route_points),
        "is_archived": s.is_archived  # add this field to send archive status
    } for s in safaris])

# GET safari package by ID, exclude archived as well
@app.route("/safaris/<int:id>", methods=["GET"])
def get_safari_by_id(id):
    s = SafariPackage.query.filter_by(id=id, is_archived=False).first_or_404()
    return jsonify({
        "id": s.id,
        "title": s.title,
        "priceRange": s.price_range,
        "location": s.location,
        "imageUrl": s.image_url,
        "rating": s.rating,
        "reviews": s.reviews,
        "description": s.description,
        "routeMap": s.route_map,
        "overview": s.overview,
        "dayByDay": s.day_by_day,
        "rates": s.rates,
        "inclusions": s.inclusions,
        "gettingThere": s.getting_there,
        "offeredBy": s.offered_by,
        "tourFeatures": safe_json_parse(s.tour_features),
        "routeDetails": s.route_details,
        "routePoints": safe_json_parse(s.route_points)
    })


# POST new safari package(s)
@app.route("/api/safaris", methods=["POST"])
def add_safari_or_safaris():
    data = request.get_json()

    if isinstance(data, dict):
        safaris = [data]
    elif isinstance(data, list):
        safaris = data
    else:
        return jsonify({"error": "Invalid input format"}), 400

    created = []
    for item in safaris:
        try:
            tour_features = item.get("tour_features")
            if isinstance(tour_features, list):
                tour_features = json.dumps(tour_features)

            route_points = item.get("route_points")
            if isinstance(route_points, list):
                route_points = json.dumps(route_points)

            new_safari = SafariPackage(
                title=item["title"],
                price_range=item.get("price_range"),
                location=item.get("location"),
                image_url=item.get("image_url"),
                rating=item.get("rating"),
                reviews=item.get("reviews"),
                description=item.get("description"),
                route_map=item.get("route_map"),
                overview=item.get("overview"),
                day_by_day=item.get("day_by_day"),
                rates=item.get("rates"),
                inclusions=item.get("inclusions"),
                getting_there=item.get("getting_there"),
                offered_by=item.get("offered_by"),
                tour_features=tour_features,
                route_details=item.get("route_details"),
                route_points=route_points
            )
            db.session.add(new_safari)
            created.append(new_safari)
        except KeyError as e:
            return jsonify({"error": f"Missing field: {e}"}), 400

    db.session.commit()
    return jsonify({"message": f"{len(created)} safari package(s) added successfully"}), 201

@app.route("/safaris/<int:safari_id>", methods=["PATCH"])
def update_safari(safari_id):
    data = request.get_json()
    safari = SafariPackage.query.get_or_404(safari_id)

    try:
        for field in [
            "title", "price_range", "location", "image_url", "rating", "reviews",
            "description", "route_map", "overview", "day_by_day", "rates",
            "inclusions", "getting_there", "offered_by", "tour_features",
            "route_details", "route_points"
        ]:
            if field in data:
                value = data[field]
                # If tour_features or route_points is a list, serialize it
                if field in ["tour_features", "route_points"] and isinstance(value, list):
                    value = json.dumps(value)
                setattr(safari, field, value)

        db.session.commit()
        return jsonify({"message": "Safari package updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@app.route("/safaris/<int:safari_id>/archive", methods=["PATCH"])
def toggle_archive_safari(safari_id):
    safari = SafariPackage.query.get_or_404(safari_id)
    safari.is_archived = not safari.is_archived  # toggle
    db.session.commit()
    return jsonify({
        "message": f"Safari package {'archived' if safari.is_archived else 'unarchived'} successfully",
        "is_archived": safari.is_archived
    })

@app.route("/safaris/<int:safari_id>/unarchive", methods=["PATCH"])
def unarchive_safari(safari_id):
    safari = SafariPackage.query.get_or_404(safari_id)

    if not safari.is_archived:
        return jsonify({"message": "Safari package is already active", "is_archived": False}), 200

    safari.is_archived = False
    db.session.commit()
    return jsonify({
        "message": "Safari package unarchived successfully",
        "is_archived": safari.is_archived
    }), 200


@app.route("/send-charter-quote", methods=["POST"])
def send_charter_quote():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        user = data.get("user")
        required_user_fields = ["fullName", "email", "phone"]
        for field in required_user_fields:
            if not user or not user.get(field):
                return jsonify({"error": f"Missing user field: {field}"}), 400

        # Email content
        email_html = f"""
        <h2>New Air Charter Quote</h2>
        <p><strong>Aircraft Type:</strong> {data.get("aircraftType")}</p>
        <p><strong>Departure:</strong> {data.get("departure")}</p>
        <p><strong>Destination:</strong> {data.get("destination")}</p>
        <p><strong>Departure Date:</strong> {data.get("departureDate")}</p>
        <p><strong>Departure Time:</strong> {data.get("departureTime")}</p>
        <p><strong>Return Date:</strong> {data.get("returnDate") or "N/A"}</p>
        <p><strong>Return Time:</strong> {data.get("returnTime") or "N/A"}</p>
        <hr/>
        <p><strong>Name:</strong> {user.get("fullName")}</p>
        <p><strong>Email:</strong> {user.get("email")}</p>
        <p><strong>Phone:</strong> {user.get("phone")}</p>
        """

        msg = Message(
            subject="New Charter Quote Request",
            recipients=["reservations@ecobeasttravels.com"]
        )
        msg.html = email_html
        mail.send(msg)

        return jsonify({"message": "Charter quote sent successfully"}), 200

    except Exception as e:
        print("Error sending charter quote:", e)
        return jsonify({"error": "Failed to send email."}), 500

  

@app.route("/send-quote", methods=["POST"])
def send_quote():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Ensure all fields exist in the request
        safari_data = data.get("safari")
        if not safari_data or not safari_data.get("id"):
            return jsonify({"error": "Safari ID not provided"}), 400

        user_details = data.get("user")
        if not user_details:
            return jsonify({"error": "User details not provided"}), 400

        required_fields = ["fullName", "email", "country", "phone", "message"]
        for field in required_fields:
            if not user_details.get(field):
                return jsonify({"error": f"Missing user field: {field}"}), 400

        start_date = data.get("startDate")
        end_date = data.get("endDate")
        if not start_date or not end_date:
            return jsonify({"error": "Start and End dates are required"}), 400

        # Query safari from DB
        safari_id = safari_data["id"]
        safari = SafariPackage.query.get_or_404(safari_id)

        # Get the safari image URL from the database model
        safari_image_url = safari.image_url  # Correctly using 'image_url' from the model

        # Get the HTML content from the request
        email_html = data.get("emailHTML")
        if not email_html:
            return jsonify({"error": "Email HTML content is missing"}), 400

        # Prepare and send email (using HTML content)
        msg = Message(
            subject="New Safari Quote Request",
            recipients=["info@ecobeasttravels.com"]  # Adjust recipient as necessary
        )
        msg.html = email_html  # Send the email with HTML content

        # You can also send plain text as a fallback if needed
        msg.body = f"""
        Quote request from: {user_details['fullName']}
        Email: {user_details['email']}
        Country: {user_details['country']}
        Phone: {user_details['phone']}
        Message: {user_details['message']}

        --- Safari Selected ---
        Title: {safari.title}
        Location: {safari.location}
        Price: {safari.price_range}
        Dates: {start_date} to {end_date}
        Travelers: {data['travelers']}
        Image URL: {safari_image_url}  # click here to see image of the package selected
        """

        # Send email using Flask-Mail
        mail.send(msg)

        return jsonify({"message": "Quote sent successfully"}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"}), 400
    except Exception as e:
        print("Email error:", e)
        return jsonify({"error": f"Failed to send quote: {str(e)}"}), 500
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(129), nullable=False)
    role = db.Column(db.String(50), default='user')
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": str(self.created_at),
        }
# Signup Resource
class Users(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response({"message": "No input data provided"}, 400)
        
        if User.query.filter_by(email=data.get('email')).first():
            return make_response({"message": "Email already taken"}, 422)

        hashed_password = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=hashed_password,
            role=data.get("role", "user")
        )
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=new_user.id)
        return make_response({
            "user": new_user.to_dict(),
            "access_token": access_token,
            "success": True,
            "message": "User has been created successfully"
        }, 201)

    @jwt_required()
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return make_response({"count": len(users_list), "users": users_list}, 200)

# Login Resource
class Login(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response({"message": "No input data provided"}, 400)

        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            return make_response({
                "user": user.to_dict(),
                "access_token": access_token,
                "success": True,
                "message": "Login successful"
            }, 200)

        return make_response({"message": "Invalid credentials"}, 401)

# Verify token resource
class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if user:
            return make_response({
                "user": user.to_dict(),
                "success": True,
                "message": "Token is valid"
            }, 200)
        return make_response({"message": "Invalid token"}, 401)

# Register routes
api.add_resource(Users, "/api/users")
api.add_resource(Login, "/api/login")
api.add_resource(VerifyToken, "/api/verify-token")




if __name__ == "__main__":
    # Only run the development server locally
    if os.environ.get("RAILWAY_ENVIRONMENT") is None:
        app.run(debug=True)