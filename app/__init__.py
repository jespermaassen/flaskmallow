import os
from dotenv import load_dotenv

from flask import Flask

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail

# Init app
app = Flask(__name__)

# Set base-dir and load .env file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=f"{BASE_DIR}/../.env")

# Database
db_uri = f"postgresql://{os.getenv('pg_username')}:{os.getenv('pg_password')}@{os.getenv('pg_host')}:{os.getenv('pg_port')}/{os.getenv('pg_dbname')}"
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("secret_key")
app.config["USE_SESSION_FOR_NEXT"] = True
app.config["CSRF_ENABLED"] = True
app.config["USER_ENABLE_EMAIL"] = False
app.config["USER_APP_NAME"] = "FlaskMallow"

# Init Login Manager
login_manager = LoginManager(app)

# Init Database
db = SQLAlchemy(app)

# Init Admin
admin = Admin(app, template_mode="bootstrap3")

# Init Flask Mail
mail = Mail(app)

# Init Marshmallow
ma = Marshmallow(app)

# Create Migration Manager
migrate = Migrate(app, db)

from app.api import views
from app.account import views
from app.exchange import views
