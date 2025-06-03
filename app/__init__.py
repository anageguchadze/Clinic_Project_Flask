from flask import Flask
from .models import db  # სწორად ვუკავშირებთ db-ს

def create_app():
    app = Flask(__name__)
    app.secret_key = 'საიდუმლო_გასაღები'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # აუცილებლად უნდა მოხდეს INIT აქ!

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()  # ამით შეიქმნება ცხრილები ერთჯერადად

    return app
