from flask import Flask
from logger import logger


def create_app():
    logger.debug('Making an app')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://melth_user:pass@192.168.1.239:5432/melth_db'

    logger.debug('Initialisation of the DB')
    from models import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    logger.debug('Initialisation of the marshmallow')
    from models import ma
    ma.init_app(app)

    logger.debug('Initialisation of the api')
    from api import api
    api.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
