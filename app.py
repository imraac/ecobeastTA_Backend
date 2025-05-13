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

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import json
from models import SafariPackage 


# Load environment variables
load_dotenv()


# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
 


# Initialize app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
CORS(app)

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

# Helper to safely parse JSON fields
def safe_json_parse(raw):
    try:
        return json.loads(raw) if raw and raw.strip() else []
    except json.JSONDecodeError:
        return []

# GET all safari packages
@app.route("/api/safaris", methods=["GET"])
def get_safaris():
    safaris = SafariPackage.query.all()
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
        "routePoints": safe_json_parse(s.route_points)
    } for s in safaris])

# GET safari package by ID
@app.route("/api/safaris/<int:id>", methods=["GET"])
def get_safari_by_id(id):
    s = SafariPackage.query.get_or_404(id)
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

@app.route("/api/send-quote", methods=["POST"])
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
            recipients=["2407984@students.kcau.ac.ke"]  # Adjust recipient as necessary
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
