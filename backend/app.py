from flask import Flask,jsonify,request

import os
import psycopg2

conn = psycopg2.connect(
        host="fv-db",
        user="postgres",
        password="my_example")

cur = conn.cursor()

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "Message": "app up and running successfully"
        })

@app.route("/make_table")
def make_table():
    return jsonify({
        "Message": "ta funkcjonalnosc juz nie jest obslugiwana"
        })


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
