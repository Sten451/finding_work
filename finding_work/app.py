import logging
from flask import Flask
from finding_work.config import Config
from finding_work.models import db, csrf, login_manager
from finding_work.main.routes import main
from finding_work.user.routes import user


app = Flask(__name__)

logging.basicConfig(filename='LOG.log', encoding='utf-8')

app.config.from_object(Config)

app.register_blueprint(main)
app.register_blueprint(user)

login_manager.init_app(app)
csrf.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
