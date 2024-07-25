from flask import Flask, request, jsonify, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if Users.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    user = Users.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"error": "Invalid username or password"}), 401
    login_user(user)
    return jsonify({"message": "Logged in successfully"}), 200

@app.route("/logout")
@login_required  # Ensure the user is logged in before they can logout
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Home Page"}), 200

if __name__ == "__main__":
    app.run()
