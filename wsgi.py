from app import app
from flask import Response

def handler(event, context):
    """Función handler para Netlify Functions"""
    return Response(
        app(event, context),
        mimetype='text/html'
    )

if __name__ == "__main__":
    app.run()
