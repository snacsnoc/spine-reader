from image_processing import ImageProcessing
from werkzeug.datastructures import FileStorage
from io import BytesIO
import base64
import pyheif
from PIL import Image


class SocketHandlers:
    def __init__(self, socketio):
        self.socketio = socketio

        @socketio.on("upload_image", namespace="/status")
        def handle_image_upload(message):
            socketio.emit(
                "status_update", {"message": "Uploading image"}, namespace="/status"
            )
            base64Image = message["image"]

            # Convert the base64 string back to bytes
            image_data = base64Image.split(",")[1].encode()
            image_bytes = base64.decodebytes(image_data)

            # Check if it's a HEIC image (iPhone)
            mime_type = base64Image.split(",")[0].split(";")[0].split(":")[1]
            if mime_type == "image/heic":
                heif_file = pyheif.read(image_bytes)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                )
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_bytes = buffered.getvalue()

            # Convert bytes to a FileStorage object
            image_file = FileStorage(
                stream=BytesIO(image_bytes),
                filename="spine_imgs/uploaded_image.png",
                content_type="image/png",
            )
            titles = ImageProcessing.process_image(image_file, self.socketio)
            socketio.emit("titles_update", {"titles": titles}, namespace="/status")
