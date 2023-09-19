# Use an official Nginx runtimae as the base image
FROM docker.io/python:3.10

# Update the package list and install Git
RUN apt update && apt install -y git

# Install Python, pip3
RUN apt install -y python3
RUN apt install -y pip

# Create a directory for your project
WORKDIR /root/production

# Clone the Quiz app repo into the container
RUN git clone https://github.com/christopher-ga/recurse-quiz-app.git

# Change to the local repo
WORKDIR /root/production/recurse-quiz-app

# Install (systemwide) the packages necessary for the Flask quiz app to run
RUN apt install -y gunicorn python3-gunicorn python3-eventlet python3-dotenv python3-flask python3-flask-migrate python3-flask-socketio

# Copy custom start up script that runs nginx and the flask app
COPY start_quiz.sh /root/production/recurse-quiz-app/start_quiz.sh
RUN chmod u+x /root/production/recurse-quiz-app/start_quiz.sh

# Run the quiz Flask app
CMD ["/root/production/recurse-quiz-app/start_quiz.sh"]