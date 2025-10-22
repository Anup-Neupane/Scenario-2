from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return {
        "message": "Hello from Simple App!",
        "version": "1.0.0",
        "environment": os.getenv('ENVIRONMENT', 'development')
    }

@app.route('/health')
def health():
    return {"status": "healthy"}

@app.route('/info')
def info():
    return {
        "app": "Simple Python App",
        "maintainer": "DevOps Team",
        "language": "Python"
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
