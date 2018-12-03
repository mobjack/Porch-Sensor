#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

@app.route('/api/v1.0/porch', methods=['GET'])
def index():
    return "Hello Eric"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
