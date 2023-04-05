import string
import random
from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello, World!'

# if __name__ == '__main__':
#     app.run()

#store short url in memory
url_mapping = {}

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
        while short_url in url_mapping:
            short_url = generate_short_url()
        url_mapping[short_url] = long_url
        response = {
            'short_url': f'http://{request.host}/{short_url}'
        }
        return jsonify(response),201
    else:
        return jsonify({'error':'Invalid long url provided'}),400


if __name__ == '__main__':
    app.run(debug=True)

