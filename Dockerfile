# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Flask runs on (Fly.io expects 8080)
EXPOSE 8080

# Run the application with Gunicorn (remove the extra CMD)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]

