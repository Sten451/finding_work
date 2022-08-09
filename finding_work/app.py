from flask import Flask
from finding_work.finding_work.config import Config
from finding_work.finding_work.models import db, csrf
from finding_work.finding_work.main.routes import main
import logging


app = Flask(__name__)

logging.basicConfig(filename='LOG.log', encoding='utf-8')

app.config.from_object(Config)

app.register_blueprint(main)
csrf.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
