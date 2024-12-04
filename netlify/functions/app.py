from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from app import app, db, login_required
import json

def handler(event, context):
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    with app.test_client() as client:
        # Rutas principales
        if path == '/':
            response = client.get('/')
        elif path == '/admin':
            response = client.get('/admin')
        elif path == '/login':
            if http_method == 'POST':
                body = json.loads(event.get('body', '{}'))
                response = client.post('/login', json=body)
            else:
                response = client.get('/login')
        elif path.startswith('/guardar'):
            body = json.loads(event.get('body', '{}'))
            response = client.post('/guardar', json=body)
        elif path.startswith('/editar_registro/'):
            id = path.split('/')[-1]
            if http_method == 'POST':
                body = json.loads(event.get('body', '{}'))
                response = client.post(f'/editar_registro/{id}', json=body)
            else:
                response = client.get(f'/editar_registro/{id}')
        elif path.startswith('/eliminar_registro/'):
            id = path.split('/')[-1]
            response = client.delete(f'/eliminar_registro/{id}')
        else:
            response = client.get(path)

        return {
            'statusCode': response.status_code,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': response.get_data(as_text=True)
        }
