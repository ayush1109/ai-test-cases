# run.py
from app import app

if __name__ == '__main__':
    port = 10000  # Use Railway's PORT
    app.run(host="0.0.0.0", port=port)
