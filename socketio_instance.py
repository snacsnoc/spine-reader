class SocketIOInstance:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocketIOInstance, cls).__new__(cls)
            cls._instance._socketio = None
        return cls._instance

    @property
    def socketio(self):
        return self._socketio

    @socketio.setter
    def socketio(self, socketio_instance):
        self._socketio = socketio_instance
