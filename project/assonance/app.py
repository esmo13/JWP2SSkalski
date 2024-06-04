from flask import Flask
from flask_cors import CORS, cross_origin
from config import Config
from models import db
from controllers import users_bp

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(users_bp)

if __name__ == '__main__':
    app.run(host='localhost', port=44338, debug=True)