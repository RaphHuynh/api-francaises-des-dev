FROM python:3.11

WORKDIR /home
RUN mkdir /home/app
COPY app /home/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]