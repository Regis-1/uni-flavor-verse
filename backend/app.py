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

@app.route("/przepisy")
def fetch_all_przepisy():
    query = "select id, nazwa, opis, poziom_trudnosci, kalorycznosc from przepis;"
    cur.execute(query)
    przepisy = cur.fetchall()
    return jsonify(przepisy)

@app.route("/przepisy/<int:id>", methods=['GET', 'POST', 'DELETE'])
def fetch_przepis_with_id(id):
    if request.method == 'GET':
        query = f"select * from przepis where id = {id};"
        cur.execute(query)
        przepis = cur.fetchone()
        return jsonify(przepis)
    elif request.method == 'POST':
        dane = request.json
        return jsonify(
            {
                "Message": "probowałeś update'ować przepis",
                "Twoje nowe hasło": request.form.get("nowe_haslo")
            }
        )
    else:
        return jsonify({"Message": "nie obsługiwana metoda"})


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
