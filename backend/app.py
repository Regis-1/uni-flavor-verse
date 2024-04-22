from flask import Flask,jsonify,request

import psycopg2

conn = psycopg2.connect(
        host="fv-db",
        user="postgres",
        password="my_example")

cur = conn.cursor()

app = Flask(__name__)

def create_przepis_from_json(json_data):
    if not json_data:
        return {"Message": "Błędny format JSON!"}

    #checking for all necessary fields
    #id?, autor, nazwa, poziom_trudnosci, procedura_wykonania
    necessary_fields = ["autor", "nazwa", "poziom_trudnosci", "procedura_wykonania"]
    fields = {
            "autor": None,
            "nazwa": None,
            "opis": None,
            "poziom_trudnosci": None,
            "procedura_wykonania": None,
            "kalorycznosc": None
    }
    for k, v in fields.items():
        v = json_data.get(k)
        fields[k] = v
        if (not v) and (k in necessary_fields):
            return {"Message": f"Brakujące dane do stworzenia nowego przepisu: {k}"}
    
    #query builder
    query_elements = (
            'insert into Przepis(autor,nazwa,poziom_trudnosci,procedura_wykonania',
            '' if not fields['opis'] else ',opis',
            '' if not fields['kalorycznosc'] else ',kalorycznosc',
            ') values (',
            "{}, '{}', {}, '{}'".format(fields['autor'],fields['nazwa'],
                 fields['poziom_trudnosci'],fields['procedura_wykonania']),
            '' if not fields['opis'] else ",'{}'".format(fields['opis']),
            '' if not fields['kalorycznosc'] else ",{}".format(fields['kalorycznosc']),
            ');')

    query = ''.join(query_elements)
    
    cur.execute(query)
    conn.commit()
    return {
            "Message": "Przepis został poprawnie dodany",
            "Query": query
            } 


@app.route("/")
def home():
    return jsonify({
        "Message": "Witamy REST API flavor-verse - internetowej bazy danych z przepisami kulinarnymi"
        })


@app.route("/api/przepisy/", methods=['GET'])
def fetch_all_przepisy():
    query = "select id, nazwa, opis, poziom_trudnosci, kalorycznosc from przepis;"
    cur.execute(query)
    przepisy = cur.fetchall()
    return jsonify(przepisy)


@app.route("/api/przepisy/<int:id>", methods=['GET'])
def fetch_przepis_with_id(id):
    query = f"select * from przepis where id = {id};"
    cur.execute(query)
    przepis = cur.fetchone()
    return jsonify(przepis)


@app.route("/api/przepisy/", methods=['POST'])
def create_new_przepis():
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        rd = create_przepis_from_json(request.get_json())
        return jsonify(rd)


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
