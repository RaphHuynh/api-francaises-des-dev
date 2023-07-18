FROM python:3.11

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv /opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /home
COPY app ./app
COPY requirements.txt ./requirements.txt
COPY docker .
COPY bd ./bd
RUN pip install --no-cache-dir -r requirements.txt


# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]