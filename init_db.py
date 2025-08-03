# init_db.py
from app import app, db
from models import *
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Tables created.")
