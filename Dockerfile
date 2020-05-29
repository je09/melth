FROM python:3.7.4-buster
COPY src /melth
COPY requirements.txt /
RUN pip install -r /requirements.txt
WORKDIR /melth
EXPOSE 8003

CMD ["gunicorn", "--bind", "0.0.0.0:8003", "app:create_app()"]
