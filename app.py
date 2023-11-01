from flask import Flask, render_template
from flask_socketio import SocketIO
import os

from socketio_instance import SocketIOInstance
from socket_handlers import SocketHandlers


class Configuration:
    def __init__(self):
        if "OPENAI_API_KEY" not in os.environ:
            raise EnvironmentError("OPENAI_API_KEY is not set in the environment!")


class FlaskApplication:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "some_secret_key"
        self.socketio = SocketIO(self.app, ping_timeout=120)

        # Set the socketio instance in the Singleton
        socketio_instance = SocketIOInstance()
        socketio_instance.socketio = self.socketio

        # Configuration initialization
        Configuration()

        # SocketHandlers
        self.socket_handlers = SocketHandlers(self.socketio)

        # Flask Routes
        FlaskRoutes(self.app, self.socket_handlers)

    def run(self):
        self.socketio.run(self.app, debug=True, allow_unsafe_werkzeug=True)


class FlaskRoutes:
    def __init__(self, app, socket_handlers):
        @app.route("/", methods=["GET", "POST"])
        def index():
            return render_template("index.html")


application = FlaskApplication()
app = application.app

if __name__ == "__main__":
    application.run()
