from flask import jsonify, request
from db_utils import (create_from_json, read_columns_from_table, 
    update_from_json, delete_record_from_table, cur)
from . import bp_przepisy

# get all przepisy from the database
@bp_przepisy.route("/api/przepisy/", methods=['GET'])
def fetch_all_przepisy():
    columns = ['id','nazwa','opis','poziom_trudnosci','kalorycznosc']
    results = read_columns_from_table('przepis', columns)
    return jsonify(results)


# get specific przepis from the database
@bp_przepisy.route("/api/przepisy/<int:id>", methods=['GET'])
def fetch_przepis_with_id(id):
    columns = ['id', 'autor', 'nazwa','opis','poziom_trudnosci',
        'procedura_wykonania', 'kalorycznosc']
    result = read_columns_from_table('przepis', columns,
        f'id = {id}', True)
    return jsonify(result)


# create new przepis via the POST HTTP method
@bp_przepisy.route("/api/przepisy/", methods=['POST'])
def create_new_przepis():
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        result = create_from_json(request.get_json(), 'Przepis')
        return jsonify({
            "Message": result[0],
            "ID": result[1]
        })


# delete specific przepis with id from the database
@bp_przepisy.route("/api/przepisy/<int:id>", methods=['DELETE'])
def delete_selected_przepis(id):
    delete_record_from_table('przepis', f'id={id}')
    return jsonify({
        "Message": f"Przepis o id = {id} został usunięty z bazy danych"
    })


# update specific przepis with id and JSON data
@bp_przepisy.route("/api/przepisy/<int:id>", methods=['PUT'])
def update_selected_przepis(id):
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = update_from_json(request.get_json(), 'Przepis', f'id={id}')
        return jsonify({
            "Message": message
        })

# read all skladniki for specific przepis with id
@bp_przepisy.route("/api/przepisy/skladniki/<int:id>", methods=['GET'])
def fetch_all_skladniki_przepisu(id):
    query = ("select s.id, s.nazwa as nazwa from Przepis_skladniki ps"
             " inner join Przepis p on ps.przepis = p.id"
             " inner join Skladnik s on ps.skladnik = s.id"
             f" where p.id = {id};")
    cur.execute(query)
    results = cur.fetchall()
    results = [{"id":r[0], "nazwa":r[1]} for r in results]
    return jsonify(results)
