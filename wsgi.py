from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from app import app

# Mount Flask app under /meseri prefix
# This makes url_for() generate URLs like /meseri/static/...
app.config['APPLICATION_ROOT'] = '/meseri'
application = DispatcherMiddleware(None, {
    '/meseri': app
})

if __name__ == '__main__':
    run_simple('0.0.0.0', 5001, application)
