import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_username = "myuser" #os.environ["DB_USERNAME"]
db_password = "mypassword" #os.environ["DB_PASSWORD"]
db_host = os.environ.get("DB_HOST", "127.0.0.1")
db_port = os.environ.get("DB_PORT", "5433")
db_name = os.environ.get("DB_NAME", "mydatabase")

app = Flask(__name__)
print(f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)

# export DB_USERNAME=myuser
# export DB_PASSWORD=mypassword
# export DB_HOST=127.0.0.1
# export DB_PORT=5433
# export DB_NAME=mydatabase
