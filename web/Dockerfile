FROM python:3
COPY . .
RUN pip install -r requirements.txt

CMD export FLASK_APP=tools/app.py && flask run --host=0.0.0.0
