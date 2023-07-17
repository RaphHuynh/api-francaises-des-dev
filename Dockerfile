FROM python:3.11

WORKDIR /home
RUN mkdir /home/app
# RUN python -m venv /home/app/venv
# ENV PATH="/home/app/venv/bin:$PATH"
COPY app /home/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]