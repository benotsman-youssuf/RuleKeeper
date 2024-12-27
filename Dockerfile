# Use a Python 3.9 image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set environment variables for the bot token and Mistral API key
# These should be provided via Docker's environment variable feature at runtime
# Alternatively, you can include a `.env` file in the container if needed
ENV DISCORD_TOKEN="your_discord_bot_token"
ENV MISTRAL_API_KEY="your_mistral_api_key"

# Expose any ports (Discord bots don't need exposed ports)
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
