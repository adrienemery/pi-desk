#!usr/bin/python
from flask import Flask, jsonify, request, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask.ext.cors import CORS


# initialize flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# allow Cross Origin Requests
CORS(app)


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
def update_digital_pin(position_id):
    """ Update the value of the digital pin specified """
    position = Position.query.get(position_id)
    print position
    return jsonify({'height': position.height}), 200


# Create the database tables.
db.create_all()

# Create the Flask-Restless API manager.
manager = APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Position, methods=['GET', 'POST', 'PATCH', 'DELETE'])


if __name__ == '__main__':
    # start the flask app
    app.run(debug=True, use_reloader=True)
