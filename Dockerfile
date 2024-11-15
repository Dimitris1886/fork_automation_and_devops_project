FROM python:3.10-slim

WORKDIR /app

# Copy requirements.txt into the container as first layer
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

ARG FREE_CURRENCY_API_KEY
ENV FREE_CURRENCY_API_KEY=${FREE_CURRENCY_API_KEY}


# Expose port 5000 for the Flask app for local testing
EXPOSE 5000

CMD ["python", "app.py"]