from flask import Flask, g
import pymongo


app = Flask(__name__)
app.config.from_object('shopcop.config')
app.config.from_envvar('SHOPCOP_CONFIG', silent=True)


def connect_db(app=None):
  "Returns a new connection to the database."
  if app is None:
    app = shopcop.app
  connection = pymongo.Connection(app.config['DATABASE_CONNECTION'])
  db = connection[app.config['DATABASE_NAME']]
  return connection, db


@app.before_request
def before_request():
  "Get a connection to the database for each request."
  g.db_connection, g.db = connect_db()


@app.after_request
def after_request(response):
  "Closes the database connection at the end of the request."
  g.db_connection.end_request()
  return response


import shopcop.views
import shopcop.tasks

shopcop.tasks.g_default_queue = shopcop.tasks.TaskQueue(dir=app.config['TASK_QUEUE_DIR'])
