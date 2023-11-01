This application uses Flask, Socket.IO, Tesseract, and EasyOCR for real-time reading of book spines. It also integrates OpenAI's GPT-3.5 Turbo/4 for better context in extracting book titles and details
# Setup and Installation
Environment Variables: Ensure the `OPENAI_API_KEY` is set in your environment.

# Dependencies:
Install required dependencies using:

```
pip install -r requirements.txt
```
Running Locally:

```
python app.py
```

# Deployment:
If deploying to Heroku, ensure you have the provided Procfile in the root directory. Use gunicorn as specified to start the web server.

# Deployment on Railway with Nix Packs

As this application is intended to operate in a headless environment, the standard opencv-python package, which comes with GUI libraries, is unnecessary. Thus, we switch to opencv-python-headless to avoid unnecessary dependencies and potential issues (missing libGL1.so)