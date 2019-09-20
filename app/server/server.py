import logging

from mongoengine import connect
from flask import Flask
from flask_socketio import SocketIO, emit

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


socketio = SocketIO(app, host='0.0.0.0', port=5000)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s]  %(message)s",
    datefmt='%H:%M:%S'
)

log = logging.getLogger(__name__)

# SocketIO response functions

log.info('Server log started, logging operations.')


# ping sockets

@socketio.on('server_ping')
def server_ping():
    log.info('Server ping received from client.')
    emit(
        'server_pong', {'data': 'Server ping received.'}
    )
    log.info('Server pong emitted to client.')


@socketio.on('db_ping')
def db_ping():
    log.info('Database ping received from client.')
    client = connect(
        host='mongodb://localhost:27017/'
    )
    log.info(
        client.server_info()
    )
    emit(
        'db_pong', {'data': 'Database ping received. Connected'}
    )
    log.info('Database pong emitted to client.')


if __name__ == "__main__":
    socketio.run(app)