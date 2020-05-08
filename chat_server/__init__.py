#!/usr/bin/env python3
from flask import Flask,render_template, request, session, Response, redirect

from typing import List

import sympy
import json
import time

if __package__ is None or __package__ == '':
    from database import connector
    from model import entities
else:
    from .database import connector
    from .model import entities


db: connector.Manager = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)


@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

# CROUT users

# 1. Create
@app.route('/users', methods=['POST'])
def create_user() -> str:
    body = json.loads(request.data)
    user = entities.User(
            username=body['username'],
            name=body['name'],
            fullname=body['fullname'],
            password=body['password'],
    )

    # Send to db
    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    # Response
    message = {'msg': "User created"}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    res = Response(json_message, status=201, mimetype="application/json")
    return res


@app.route('/users', methods=['GET'])
def read_user() -> str:
    db_session = db.getSession(engine)
    response = db_session.query(entities.User)
    users = response[:]

    json_message = json.dumps(users, cls=connector.AlchemyEncoder)

    return Response(json_message, status=200, mimetype="application/json")


@app.route('/users/<id>', methods=['PUT'])
def update_user(id: str) -> str:
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).\
        filter(entities.User.id == id).first()

    body = json.loads(request.data)
    for key in body.keys():
        setattr(user, key, body[key])

    db_session.add(user)
    db_session.commit()

    # Response
    message = {'msg': "User updated"}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    res = Response(json_message, status=201, mimetype="application/json")
    return res


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id: str) -> str:
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).\
        filter(entities.User.id == id).first()

    db_session.delete(user)
    db_session.commit()

    # Response
    message = {'msg': "User deleted"}
    json_message = json.dumps(message, cls=connector.AlchemyEncoder)
    res = Response(json_message, status=201, mimetype="application/json")
    return res


def main():
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


if __name__ == '__main__':
    main()
