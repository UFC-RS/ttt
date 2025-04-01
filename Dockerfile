#Set container base image using Python 3.11.12
FROM docker.rsint.net/docker.io/python:3.12-slim-bookworm

#Set working directory in the container
WORKDIR /app

#Copy the source code folder into the container
COPY . /app

RUN apt update && apt install -y git

#Install pip and virtualenv
RUN pip install --upgrade pip virtualenv

#Create and activate a virtual environment
RUN virtualenv venv ENV PATH="/app/venv/bin:$PATH" RUN pip install --no-cache-dir -r requirements.txt RUN pip install -e /app/

#Export the port 8000 to run the ttt application
EXPOSE 8000

#Run the ttt application
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "8000"]
