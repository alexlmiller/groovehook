from flask import Flask, render_template, request, jsonify
from werkzeug.routing import Rule
import os
import datetime
import callshopify

groove_token = os.environ.get('GROOVE_API_TOKEN')

app = Flask(__name__)

@app.route('/shopify', methods=['GET'])
def data():
    customer = request.args.get('email')
    request_token = request.args.get('api_token')
    if request_token == groove_token:
        payload = callshopify.fetchdata(customer)
        return payload, 200
    else:
        return jsonify({'status':'bad token'}), 401
