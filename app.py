from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 for Fly.io
    app.run(host="0.0.0.0", port=port)


