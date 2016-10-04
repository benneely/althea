# -*- coding: utf-8 -*-
from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World! I am the registrator, helping add models to your installation!"
    
def main():
    try:
        port = int(sys.argv[1])
    except:
        port = 8001
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()