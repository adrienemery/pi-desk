#!usr/bin/python

# system imports
import time

# flask imorts
from flask import Flask, jsonify, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask.ext.cors import CORS

from utils import Desk

# initialize flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/desk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# allow Cross Origin Requests
CORS(app)
desk = Desk()


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, height, name):
        self.height = height
        self.name = name

    def __repr__(self):
        return '{} - Height: {}'.format(self.name, self.height)


@app.route('/', methods=['GET'])
def status():
    return jsonify({'status': 'ok'})


@app.route('/api/desk/position/<int:position_id>', methods=['POST'])
def move_to_position(position_id):
    position = Position.query.get(position_id)
    desk.move(setpoint=position.height)
    return jsonify({'height': desk.height}), 200


@app.route('/api/desk/up', methods=['POST'])
def move_up():
    desk.move_up()
    return jsonify({'moving': desk.direction}), 200


@app.route('/api/desk/down', methods=['POST'])
def move_down():
    desk.move_down()
    return jsonify({'moving': desk.direction}), 200


@app.route('/api/desk/stop', methods=['POST'])
def stop():
    desk.stop()
    return jsonify({'moving': 'stopped'}), 200


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Position, methods=['GET', 'POST', 'PATCH', 'DELETE'])


if __name__ == '__main__':
    # start the flask app
    app.run(host='0.0.0.0', port=8000)
