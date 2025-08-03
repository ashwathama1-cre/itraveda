from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from models import db, User, Product, Order, Wishlist, RecentlyViewed, SellerStats
from config import Config
from dotenv import load_dotenv
load_dotenv()
from itraveda import app, db
from models import *

with app.app_context():
    db.create_all()
    print("✅ Tables created")


# ✅ Step 1: Define app BEFORE using it
app = Flask(__name__)

# ✅ Step 2: Load Config from Config class
app.config.from_object(Config)

# ✅ Optional override from environment if needed
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///itraveda.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Step 3: Initialize extensions
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# ✅ Step 4: Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ✅ Routes
@app.route('/')
def home():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("home.html", products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        unique_code = request.form.get('unique_code') or os.urandom(4).hex()

        if User.query.filter_by(email=email).first():
            flash("Email already registered", "warning")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password, role=role, unique_code=unique_code)
        db.session.add(user)
        db.session.commit()

        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        code = request.form.get('unique_code')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password) and user.unique_code == code:
            login_user(user)
            flash("Welcome!", "success")

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'seller':
                return redirect(url_for('seller_dashboard'))
            else:
                return redirect(url_for('buyer_dashboard'))
        else:
            flash("Invalid credentials or code", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('home'))
    return render_template("admin_dashboard.html")

@app.route('/seller/dashboard')
@login_required
def seller_dashboard():
    if current_user.role != 'seller':
        return redirect(url_for('home'))
    return render_template("seller_dashboard.html")

@app.route('/buyer/dashboard')
@login_required
def buyer_dashboard():
    if current_user.role != 'buyer':
        return redirect(url_for('home'))
    return render_template("buyer_dashboard.html")

# ✅ For local testing
if __name__ == '__main__':
    app.run(debug=True)
