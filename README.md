# api-francaises-des-dev
           
## To set up the project

Install dependence :

```
pip install -r requirements.txt 
```

Change .env.example to set up the database :

```
MYSQL_USER = ""
MYSQL_PASSWORD = ""
MYSQL_DATABASE = ""
MYSQL_PORT = 3306
MYSQL_HOST = "localhost"
```

remove .example extension from the file .env.example

To start the server :

```
uvicorn app.main:app --reload
```

>⚠️ You need a virtual environment -> see the FastAPI document

## Setup with docker

Requirements:
- Docker 20

For the first setup you must build the image `docker-compose build`

Start everything `docker-compose up -d`

Stop ```docker-compose stop```