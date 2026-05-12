"""
Webserver independiente para evitar que el bot se apague
(Opcional si prefieres mantenerlo separado de main.py)
"""

from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot de MundoLand activo y funcionando', 200

@app.route('/status')
def status():
    return {'status': 'online', 'message': 'Bot is running'}, 200

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=PORT)
