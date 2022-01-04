FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
