   
import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
   
   
    MAIL_SERVER = 'mail.ecobeasttravels.co.ke'  
    MAIL_PORT = 465
    MAIL_USE_SSL = True  
    MAIL_USE_TLS = False  
    MAIL_USERNAME = 'noreply@ecobeasttravels.co.ke'  
    MAIL_PASSWORD = '@#23junior'  
    MAIL_DEFAULT_SENDER = 'noreply@ecobeasttravels.co.ke'  