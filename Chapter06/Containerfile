FROM python:3.9

# Set working directory
WORKDIR /app

# Copy app.py file to container
COPY app.py .

# Install Flask
RUN pip install flask

# Expose port 5000
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
