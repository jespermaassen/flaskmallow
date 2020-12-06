from app import app, login_manager
from app.models import *
from app.enums import *
from flask_login import UserMixin, login_user, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
