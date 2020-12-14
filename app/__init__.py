import os
from dotenv import load_dotenv

from flask import Flask, jsonify

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from flask_sijax import Sijax
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.helpers import make_response
from flask_httpauth import HTTPBasicAuth

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

# Init Sijax
sijax = Sijax(app)

# Init Marshmallow
ma = Marshmallow(app)

# Init HTTPAuth
auth = HTTPBasicAuth()

# Init rate Limiter
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["500 per day", "60 per hour"]
)

# Override the 429 HTML response with a json one
@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(
            code=429,
            message="Too Many Requests",
            reason="ratelimit exceeded %s" % e.description,
        ),
        429,
    )


# Create Migration Manager
migrate = Migrate(app, db)

from app.api import views
from app.account import views
from app.exchange import views
from app.leaderboard import views