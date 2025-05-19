# run.py
from app import app
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Railway's PORT
    app.run(host="0.0.0.0", port=port)         # Bind to public host