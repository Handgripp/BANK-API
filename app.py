from flask import Flask
from extensions import db
# from controllers.user_controller import user_blueprint
# from controllers.post_controller import post_blueprint
# from controllers.follow_controller import follow_blueprint
# from controllers.comment_controller import comment_blueprint
# from controllers.auth_controller import auth_blueprint


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # app.register_blueprint(user_blueprint)
    # app.register_blueprint(post_blueprint)
    # app.register_blueprint(follow_blueprint)
    # app.register_blueprint(comment_blueprint)
    # app.register_blueprint(auth_blueprint)

    return app
