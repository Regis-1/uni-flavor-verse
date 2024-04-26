from flask import jsonify, request
from db_utils import create_from_json, read_columns_from_table, update_from_json, delete_record_from_table
from . import bp_przepisy

# get all przepisy from the database
@bp_przepisy.route("/api/przepisy/", methods=['GET'])
def fetch_all_przepisy():
    przepisy = read_columns_from_table('przepis',
        ['id','nazwa','opis','poziom_trudnosci','kalorycznosc'])
    return jsonify(przepisy)


# get specific przepis from the database
@bp_przepisy.route("/api/przepisy/<int:id>", methods=['GET'])
def fetch_przepis_with_id(id):
    przepis = read_columns_from_table('przepis', ['*'],
        f'id = {id}', True)
    return jsonify(przepis)


# create new przepis via the POST HTTP method
@bp_przepisy.route("/api/przepisy/", methods=['POST'])
def create_new_przepis():
    if not request.is_json:
        return jsonify({
            "Message": "Zły rodzaj żądania. Wymagany jest typ application/json."
        })
    else:
        message = create_from_json(request.get_json(), 'Przepis')
        return jsonify({
            "Message": message
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
