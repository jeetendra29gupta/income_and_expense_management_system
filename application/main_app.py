from flask import Flask
from application.models import db
from application.routes import bp as main_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///income_expense.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main_bp)

# Create the database
with app.app_context():
    db.create_all()
