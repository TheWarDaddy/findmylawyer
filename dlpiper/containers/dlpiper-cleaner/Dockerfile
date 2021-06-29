FROM python:3.8

WORKDIR /app

COPY lib .
COPY requirements.txt .
COPY containers/dlpiper-cleaner/wait-for-it.sh .
RUN chmod +x wait-for-it.sh
COPY containers/dlpiper-cleaner/names_cleaner.sql .
RUN chmod +x names_cleaner.sql

# set display port to avoid crash
ENV DISPLAY=:99
RUN apt-get update && apt-get install -y postgresql-contrib
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["./wait-for-it.sh", "postgres-database"]
