from dotenv import load_dotenv

from app import socketio, app


# load environment variables
load_dotenv()


if __name__ == "__main__":
    socketio.run(app, port=6002)