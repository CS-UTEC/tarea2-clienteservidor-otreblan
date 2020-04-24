#!/usr/bin/env python3
from flask import Flask,render_template, request, session, Response, redirect

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


@app.route('/create_user')
def create_user():
    user = entities.User(
        name='Alberto',
        fullname="Alberto Oporto Ames",
        password="unodostres",
        username="otreblan",
    )

    print(user)

    db_session = db.getSession(engine)
    db_session.add(user)
    db_session.commit()

    return "User created"


def main():
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


if __name__ == '__main__':
    main()
