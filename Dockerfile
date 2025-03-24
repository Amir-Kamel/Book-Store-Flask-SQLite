# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure instance directory exists
RUN mkdir -p instance && touch instance/database.db

# Expose the port Flask will run on (Railway assigns PORT dynamically)
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
