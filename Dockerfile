# Use the official Python image
FROM python:3.10-slim AS build

# Set the working directory
WORKDIR /themenufy-ai

# Copy the current directory contents into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir blinker==1.8.2 \
    click==8.1.7 \
    colorama==0.4.6 \
    Flask==3.0.3 \
    itsdangerous==2.2.0 \
    Jinja2==3.1.4 \
    MarkupSafe==2.1.5 \
    Werkzeug==3.0.3 \
    flask_cors \
    matplotlib \
    pandas \
    scikit-learn \
    requests
RUN pip install gunicorn

# Expose the port that the Flask app runs on
EXPOSE 2233

# Command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:2233", "recommendation:app"]
