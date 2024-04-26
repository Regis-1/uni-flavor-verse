from flask import jsonify, request
from db_utils import create_from_json, read_columns_from_table, update_from_json, delete_record_from_table
from . import bp_skladniki

# get all skladniki from the database
@bp_skladniki.route("/api/skladniki/", methods=['GET'])
def fetch_all_skladniki():
    skladniki = read_columns_from_table('Skladnik',['id','nazwa'])
    return jsonify(skladniki)


# get specific skladnik from the database
@bp_skladniki.route("/api/skladniki/<int:id>", methods=['GET'])
def fetch_skladnik_with_id(id):
    skladnik = read_columns_from_table('Skladnik', ['*'],
        f'id = {id}', True)
    return jsonify(skladnik)


# create new skladnik via the POST HTTP method
@bp_skladniki.route("/api/skladniki/", methods=['POST'])
def create_new_skladnik():
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = create_from_json(request.get_json(), 'Skladnik')
        return jsonify({
            "Message": message
        })


# delete specific skladnik with id from the database
@bp_skladniki.route("/api/skladniki/<int:id>", methods=['DELETE'])
def delete_selected_skladnik(id):
    delete_record_from_table('Skladnik', f'id={id}')
    return jsonify({
        "Message": f"Skladnik o id = {id} został usunięty z bazy danych"
    })


# update specific skladnik with id and JSON data
@bp_skladniki.route("/api/skladniki/<int:id>", methods=['PUT'])
def update_selected_skladnik(id):
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = update_from_json(request.get_json(), 'Skladnik', f'id={id}')
        return jsonify({
            "Message": message
        })
