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


@app.route('/espar/<n>')
def espar(n: int) -> str:
    if ((int(n) % 2) == 0):
        return 'True'
    else:
        return 'False'


@app.route('/esprimo/<n>')
def esprimo(n: str) -> str:
    return 'True' if sympy.isprime(int(n)) else 'False'


@app.route('/palindrome/<palabra>')
def palindrome(palabra: str) -> str:
    for i in range(0, int(len(palabra)/2)):
        if(palabra[i] != palabra[len(palabra)-1-i]):
            return 'False'
    return 'True'


@app.route('/multiplo/<n1>/<n2>')
def multiplo(n1: str, n2: str) -> str:
    _n1: int = int(n1)
    _n2: int = int(n2)

    if((_n1 % _n2) == 0):
        return 'True'
    else:
        return 'False'


@app.route('/create_user/<_name>/<_fullname>/<_password>/<_username>')
def create_user(_name: str, _fullname: str, _password: str, _username: str):
    user = entities.User(
        name=_name,
        fullname=_fullname,
        password=_password,
        username=_username,
    )

    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "User created"


@app.route('/read_users')
def read_users():
    db_session = db.getSession(engine)
    resp = db_session.query(entities.User)
    users: List[entities.User] = resp[:]

    resu: str = ('<table>'

                 '<tr>'
                 '<th>name</th>'
                 '<th>fullname</th>'
                 '<th>password</th>'
                 '<th>username</th>'
                 '</tr>')

    for i in users:
        resu += ('<tr>'

                 '<td>' + i.name + '</td>'
                 '<td>' + i.fullname + '</td>'
                 '<td>' + i.password + '</td>'
                 '<td>' + i.username + '</td>'

                 '</tr>')

    resu += '</table>'

    return resu


def main():
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


if __name__ == '__main__':
    main()
