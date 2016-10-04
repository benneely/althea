# -*- coding: utf-8 -*-
from flask import Flask

def main():
    app = Flask(__name__)
    @app.route('/')
    def index():
        return "Hello, World!"
        
    app.run(debug=True)

if __name__ == '__main__':
    main()
    