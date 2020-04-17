#!/usr/bin/env python3
from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
from math import sqrt
from typing import List
import json
import time

db = connector.Manager()
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
def esprimo(n: int) -> str:
    _n: int = int(n)
    if(_n == 2):
        return 'True'

    primeList: List[int] = [2]
    for i in range(3, int(sqrt(_n)+2), 2):
        isPrime: bool = True
        for j in primeList:
            if ((i % j) == 0):
                isPrime = False
                break

        if (isPrime):
            primeList.append(i)

    for i in primeList:
        if((_n % i) == 0):
            return 'False'

    return 'True'


def main():
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


if __name__ == '__main__':
    main()
