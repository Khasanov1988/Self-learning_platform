FROM python:3

WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

COPY . .
