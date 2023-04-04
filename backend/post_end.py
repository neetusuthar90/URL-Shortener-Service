import string
import random
from flask import Flask,request,jsonify

app = Flask(__name__)

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
    long_url = data.get('long url')
    if long_url:
        short_url = generate_short_url()
        while short_url in url_mapping:
            short_url = generate_short_url()
        url_mapping[short_url] = long_url
        responce = {
            'short_url': f'http://{request.host}/{short_url}'
        }
        return jsonify(responce),201
    else:
        return jsonify({'error':'Invalid url providedxx'}),400


if __name__ == '__main__':
    app.run(debug=True)