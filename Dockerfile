Вариант 1
FROM python:3.8.2

COPY requirements.txt ./
RUN pip install --requirement ./requirements.txt
COPY main.py ./
COPY data.json ./
COPY models.py ./


ENTRYPOINT uvicorn main:app --reload

# CMD ["python", "./main.py"]
