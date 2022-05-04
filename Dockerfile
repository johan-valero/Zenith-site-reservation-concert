FROM python:3
RUN apt update && apt install -y default-mysql-client
ENV PYTHONWRITECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
