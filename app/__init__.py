from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'  # დროებით, auth-ისთვის მოგვიანებით გამოვიყენებთ

    from .routes import main
    app.register_blueprint(main)

    return app
