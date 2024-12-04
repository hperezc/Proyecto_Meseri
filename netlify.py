from flask import Flask
from app import app as flask_app

def handler(event, context):
    return flask_app(event, context)
