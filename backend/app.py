from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import string
import random
import os
from validators import url
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
CORS(app)

# MySQL connection string is read from env var
connection_string = os.environ['CONNECTION_STRING']
app.config['SQLALCHEMY_DATABASE_URI'] =  connection_string

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)

# define a model

class url_mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(1024), nullable=False)
    short_url = db.Column(db.String(62), nullable=False, unique=True)

# generate short url
def generate_short_url(length=7):
    char = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(char) for _ in range(length))
    return short_url

## Create short URL and store in DB
@app.route('/shorten_url', methods=['POST'])

def shorten_url():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    long_url = data.get('long_url')
    print(long_url)
    if url(long_url):
        record = url_mapping.query.filter_by(long_url=long_url).first()
        if record is None:
            short_url = generate_short_url()
            new_url = url_mapping(long_url=long_url, short_url=short_url)
            db.session.add(new_url)
            db.session.commit()
            response = {'short_url': f'http://{request.host}/{short_url}'}
        else:
            response = {
                'short_url': f'http://{request.host}/{record.short_url}'
            }
        return jsonify(response), 201
    else:
        return jsonify({'error': 'Invalid long url provided'}), 400


## Redirect to long url
@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    record = url_mapping.query.filter_by(short_url=short_url).first()

    if not record:
        return jsonify({"error:": "Short url not found"}), 404
    else:
        return redirect(record.long_url)


if __name__ == '__main__':
    from app import db,app 
    if not database_exists(connection_string):
        create_database(connection_string)
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
