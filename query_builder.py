from app import app, db
from app.models import *

db.session.commit()
db.drop_all()
db.create_all()