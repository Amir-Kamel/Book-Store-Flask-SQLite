# Use the official lightweight Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

FROM python:3.11

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose Fly.io's default port
EXPOSE 8080

# Start the app using Gunicorn (Recommended for production)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:create_app()"]



