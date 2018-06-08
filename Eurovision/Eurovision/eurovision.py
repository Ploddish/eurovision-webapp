from app import create_app

HOST = '0.0.0.0'
PORT = 80

app = create_app()
app.run(HOST, PORT)