from flask import Flask


def create_app():
    app = Flask(__name__, template_folder='../templates')
    from .s3_routes import s3_routes
    from .ec2_routes import ec2_routes
    app.register_blueprint(s3_routes)
    app.register_blueprint(ec2_routes)

    return app
