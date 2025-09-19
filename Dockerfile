# 1) Start from a small official Python image
FROM python:3.12-slim

# 2) Install basic system tools that Python packages sometimes need
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 3) Set the working folder inside the image
WORKDIR /app

# 4) Copy dependency list first so Docker can cache installs
COPY requirements.txt /app/

# 5) Install Python packages inside the image
RUN pip install -r requirements.txt

# 6) Copy the rest of your project code into the image
COPY .. /app

# 7) Tell the app which port to listen on; Render sets PORT at runtime
ENV PORT=10000
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 8) Start the web server. GuDockerfilenicorn runs your Flask app.
#    -b is short for bind, so no double dashes needed
CMD gunicorn -b 0.0.0.0:$PORT app.web:app
