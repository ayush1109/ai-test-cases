# app/routes.py
from app import app
from flask import jsonify
import asyncio

from .demo import main

@app.route('/testcases', methods=['GET'])
def testCases():
    return asyncio.run(main())

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Welcome to the API'})

#Add more routes as needed