from flask import jsonify, request
from db_utils import create_from_json, read_columns_from_table, update_from_json, delete_record_from_table
from . import bp_uzytkownicy

# get all uzytkownicy from the database
@bp_uzytkownicy.route("/api/uzytkownicy/", methods=['GET'])
def fetch_all_uzytkownicy():
    results = read_columns_from_table('Uzytkownik',['id','nazwa_uzytkownika'])
    return jsonify(results)


# get specific uzytkownik from the database
@bp_uzytkownicy.route("/api/uzytkownicy/<int:id>", methods=['GET'])
def fetch_uzytkownik_with_id(id):
    columns = ['id', 'nazwa_uzytkownika', 'haslo']
    results = read_columns_from_table('Uzytkownik', columns,
        f'id = {id}', True)
    return jsonify(results)


# create new uzytkownik via the POST HTTP method
@bp_uzytkownicy.route("/api/uzytkownicy/", methods=['POST'])
def create_new_uzytkownik():
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = create_from_json(request.get_json(), 'Uzytkownik')
        return jsonify({
            "Message": message
        })


# delete specific uzytkownik with id from the database
@bp_uzytkownicy.route("/api/uzytkownicy/<int:id>", methods=['DELETE'])
def delete_selected_uzytkownik(id):
    delete_record_from_table('Uzytkownik', f'id={id}')
    return jsonify({
        "Message": f"Uzytkownik o id = {id} został usunięty z bazy danych"
    })


# update specific uzytkownik with id and JSON data
@bp_uzytkownicy.route("/api/uzytkownicy/<int:id>", methods=['PUT'])
def update_selected_uzytkownik(id):
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = update_from_json(request.get_json(), 'Uzytkownik', f'id={id}')
        return jsonify({
            "Message": message
        })
