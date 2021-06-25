FROM python:3.8

WORKDIR /app

COPY lib .
COPY requirements.txt .
COPY containers/dlpiper-init/wait-for-it.sh .
RUN chmod +x wait-for-it.sh

# set display port to avoid crash
ENV DISPLAY=:99
RUN apt-get update && apt-get install -y postgresql-contrib
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["./wait-for-it.sh", "postgres-database", "--", "python", "database.py"]
