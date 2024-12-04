from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json

app = Flask(__name__, 
    template_folder='templates',
    static_folder='static')
CORS(app)

def handler(event, context):
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    try:
        if path == '/':
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': render_template('formulario.html')
            }
        elif path.startswith('/static/'):
            file_path = path.replace('/static/', '')
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': open(f'static/{file_path}').read()
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
