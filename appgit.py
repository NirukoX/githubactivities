from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Database Configuration (Change 'development' to 'production' as needed)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost/gitrep")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/users", methods=["GET", "POST"])
def manage_users():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/posts/<int:user_id>", methods=["GET", "POST"])
def manage_posts(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("manage_posts", user_id=user.id))
    return render_template("posts.html", user=user)

# Initialize Database
with app.app_context():
    db.create_all()

# Run Application
if __name__ == "__main__":
    app.run(debug=True)
