from flask import Flask,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import string
import random
import os


app = Flask(__name__)

#app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysecretpassword@127.0.0.1/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#define a model
class url_mapping(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    long_url = db.Column(db.String(1024),nullable=False)
    short_url = db.Column(db.String(62),nullable=False,unique=True)

    def __repr__(self):
        return f'<url_mapping{self.short_url}>'


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello, World!'

# if __name__ == '__main__':
#     app.run()

#store short url in memory
#url_mapping = {}

#generate short url
def generate_short_url(length=7):
    char = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(char) for _ in range(length))
    return short_url


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    long_url = data.get('long_url')
    if long_url:
        short_url = generate_short_url()
        while url_mapping.query.filter_by(short_url=short_url).first() is not None:
            short_url = generate_short_url()
        
        new_url = url_mapping(long_url=long_url,short_url=short_url)
        db.session.add(new_url)
        db.session.commit()

        response = {
            'short_url': f'http://{request.host}/{short_url}'
        }
        return jsonify(response),201
    else:
        return jsonify({'error':'Invalid long url provided'}),400


@app.route('/<short_url>',methods=['GET'])
def redirect_url(short_url):
    long_url = url_mapping.query.filter_by(short_url=short_url).first()
    if not long_url:
        return jsonify({"error:":"Short url not found"}),404
    else:
        return redirect(long_url)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ.get('PORT',5000))

