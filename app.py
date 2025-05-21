from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from auth import auth
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
JWTManager(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(routes, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
