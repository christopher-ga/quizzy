from dotenv import load_dotenv

from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_socketio import SocketIO, send

# app can be deployed running 'flask run' in terminal OR running 'python3 wsgi.py'
# 'python3 wsgi.py' is recommended

# config layout containing 'secret key'
from .config import Config

# importing blueprints from api directory
from .api.game_room_page import game_room_page
from .api.join_game_page import join_game_page
from .api.question_page import question_page

# import socket events from socket_events.py
from .socket_events import define_socket_events

# load environment variables
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, manage_session=False, async_mode='eventlet')
app.config.from_object(Config)

# registering blueprint pages where url_prefix is access point to web page - http://127.0.0.1:6002/gameroom etc.
app.register_blueprint(join_game_page, url_prefix='/')
app.register_blueprint(game_room_page, url_prefix='/gameroompage')
app.register_blueprint(question_page, url_prefix='/questionpage')

port = 6002
print(f"Running on http://localhost:{port}/")


# if unable to find page, load error template
@app.errorhandler(404)
def not_found(err):
    return render_template('404.html')


# calling function defined in the socket_events.py and passing socketio server import
define_socket_events(socketio)
