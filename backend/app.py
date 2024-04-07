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
    cur.execute("""create table my_table(
id integer unique not null,
note varchar(64) not null);""")

    cur.execute("""insert into my_table(id, note) values
(1, 'hello there'), (2, 'hello world');""")

    conn.commit()
    return jsonify({
        "Message": "table was successfully made"
        })


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
