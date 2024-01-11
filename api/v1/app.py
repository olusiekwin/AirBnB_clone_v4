#!/usr/bin/python3
"""
Module docs
"""
from api.v1.views import app_views
from flasgger import Swagger
from flasgger.utils import swag_from
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """
    Function Docs
    """
    return storage.close()


@app.errorhandler(404)
def error(error):
    """
    Function Docs
    """
    return jsonify({"error": "Not found"}), 404


app.config['SWAGGER'] = {
        'title': 'AirBnB clone Restful API',
        'uiversion': 3
        }

Swagger(app)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
