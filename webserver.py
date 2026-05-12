# Este archivo es OPCIONAL. El webserver está integrado en main.py
# Si deseas usar este archivo por separado, descomenta las líneas en main.py:
# from webserver import keep_alive
# keep_alive()

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def index():
    return '✅ Bot activo – Mutation\'s Network'

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    """Inicia el servidor web en un thread separado"""
    server = Thread(target=run, daemon=True)
    server.start()
