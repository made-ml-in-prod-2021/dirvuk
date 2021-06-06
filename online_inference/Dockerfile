FROM python:3.9-slim

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY model/model.pkl model/model.pkl
COPY src/app.py src/app.py

WORKDIR .

CMD ["python3", "src/app.py"]