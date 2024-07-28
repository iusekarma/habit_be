from flask import Flask
from config import Config
from routes import routes_all, jwt
from models import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    cors = CORS(app, resources={'/*':{'origins':'*'}})
    
    db.init_app(app)
    jwt.init_app(app)
    
    app.register_blueprint(routes_all, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
