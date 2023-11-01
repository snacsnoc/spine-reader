import os
import tempfile
from PIL import Image
import betterocr

from socketio_instance import SocketIOInstance
from redirect_prints import RedirectPrints


class ImageProcessing:
    MESSAGES = {
        "job_tesseract_ocr": "Running Tesseract OCR",
        "job_easy_ocr": "Running Easy OCR",
        "Combine and correct OCR results": "Generating results from AI",
        "LLM": "Received data from AI",
        "{'data':": "Done!",
    }

    @classmethod
    def handle_ocr_prints(cls, text):
        socketio = SocketIOInstance().socketio

        for line in text.splitlines():
            message = next(
                (cls.MESSAGES[key] for key in cls.MESSAGES if key in line), line
            )
            socketio.emit("status_update", {"message": message}, namespace="/status")

    @staticmethod
    def process_image(file_or_path, socketio):
        socketio.emit(
            "status_update",
            {"message": "Processing image, rotating"},
            namespace="/status",
        )

        # Create a temporary file to save the uploaded image
        temp_filename = tempfile.mktemp(suffix=".png")

        with Image.open(file_or_path) as img:
            img.rotate(90, expand=True).save(temp_filename, format="PNG")

        # Get print calls from betterocr and send as websocket messages
        with RedirectPrints() as rp:
            text = betterocr.detect_text(
                temp_filename,
                ["en"],
                context="",
                tesseract={"config": "--tessdata-dir ./tessdata"},
                openai={"model": "gpt-4"},
            )

        ImageProcessing.handle_ocr_prints(rp.get_output())

        # Remove the temporary file after processing
        os.remove(temp_filename)

        return text.split("\n")
