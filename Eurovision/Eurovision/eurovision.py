from app import create_app
from app import server_data

HOST = '0.0.0.0'
PORT = 80

app = create_app()

app.run(HOST, PORT)