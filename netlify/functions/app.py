from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json
from app import app as flask_app

def handler(event, context):
    """Handler function for Netlify Functions"""
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    
    try:
        return flask_app(event, context)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
