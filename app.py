from flask import Flask
from api import api_bp
from data_manager.data_models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.root_path}\data_manager/moviewebapp.db'
db.init_app(app)
app.register_blueprint(api_bp)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


