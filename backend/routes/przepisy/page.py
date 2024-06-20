from flask import jsonify, request, render_template, redirect, url_for
from db_utils import (create_from_json, read_columns_from_table, 
    update_from_json, delete_record_from_table, cur, conn)
from . import bp_przepisy

# get all przepisy from the database
@bp_przepisy.route("/api/przepisy/", methods=['GET'])
def fetch_all_przepisy():
    columns = ['id','obraz','nazwa','opis','poziom_trudnosci','kalorycznosc']
    results = read_columns_from_table('przepis', columns)
    return render_template('przepisy.html', przepisy=results)


# get specific przepis from the database
@bp_przepisy.route("/api/przepisy/<int:id>", methods=['GET', 'POST'])
def fetch_przepis_with_id(id):

    if request.method == "GET":

        query = ("select p.id, p.obraz, p.nazwa, p.opis, p.poziom_trudnosci, p.procedura_wykonania, p.kalorycznosc, ("
	    "select array_agg("
	    "json_build_object("
	    "'nazwa', s.nazwa,"
	    "'ilosc', ps.ilosc,"
	    "'miara', ps.miara)) "
	    "from przepis_skladniki ps "
	    "left join skladnik s on s.id = ps.skladnik "
	    f"where ps.przepis={id}"
	    ") as skladniki "
	    "from przepis p "
	    f"where p.id={id};")
        cur.execute(query)
        results = cur.fetchall()
        result = [{"id":r[0], "obraz":r[1], "nazwa":r[2], "opis":r[3], "poziom_trudnosci":r[4], "procedura_wykonania":r[5],"kalorycznosc":r[6], "skladniki":r[7]} for r in results]
        przepis=result[0]
        return render_template('przepis.html', przepis=przepis)
    
    else :
        delete_record_from_table('przepis', f'id={id}')
        return redirect(url_for('przepisy.fetch_all_przepisy'))

# update specific przepis with id and JSON data
@bp_przepisy.route("/api/przepisy/<int:id>/edit", methods=['GET', 'POST'])
def update_selected_przepis(id):
    if request.method == 'GET':

        query = ("select p.id, p.obraz, p.nazwa, p.opis, p.poziom_trudnosci, p.procedura_wykonania, p.kalorycznosc, ("
	    "select array_agg("
	    "json_build_object("
	    "'nazwa', s.nazwa,"
	    "'ilosc', ps.ilosc,"
	    "'miara', ps.miara)) "
	    "from przepis_skladniki ps "
	    "left join skladnik s on s.id = ps.skladnik "
	    f"where ps.przepis={id}"
	    ") as skladniki "
	    "from przepis p "
	    f"where p.id={id};")
        cur.execute(query)
        results = cur.fetchall()
        result = [{"id":r[0], "obraz":r[1], "nazwa":r[2], "opis":r[3], "poziom_trudnosci":r[4], "procedura_wykonania":r[5],"kalorycznosc":r[6], "skladniki":r[7]} for r in results]
        przepis=result[0]
        return render_template('przepis_edit.html', przepis=przepis)
    else:
        data = request.form
        query = ("UPDATE przepis "
                 f"SET opis = '{data['opis']}', "
                 f"nazwa = '{data['nazwa']}', "
                 f"obraz = '{data['obraz']}', "
                 f"procedura_wykonania = '{data['procedura_wykonania']}', "
                 f"kalorycznosc = {data['kalorycznosc']}, "
                 f"poziom_trudnosci = {data['poziom_trudnosci']} "
                 f" WHERE id={id};")
        cur.execute(query)
        conn.commit()
        return redirect(url_for('przepisy.fetch_przepis_with_id', id=id))
    
# create new przepis 
@bp_przepisy.route("/api/przepisy/create", methods=['GET', 'POST'])
def create_new_przepis():
    if request.method == 'GET':
        return render_template('przepis_create.html')
    else:
        data = request.form
        # updates = {
        #     'opis' : data['opis'],
        #     'nazwa' : data['nazwa'],
        #     'obraz' : data['obraz'],
        #     'procedura_wykonania' : data['procedura_wykonania'],
        #     'kalorycznosc' : data['kalorycznosc'],
        #     'poziom_trudnosci' : data['poziom_trudnosci'],
        #     'autor': 1
        # }
        query = ("INSERT INTO przepis(autor, opis, nazwa, obraz, procedura_wykonania, kalorycznosc, poziom_trudnosci) "
                f"VALUES (1, '{data['opis']}','{data['nazwa']}','{data['obraz']}','{data['procedura_wykonania']}',{data['kalorycznosc']},{data['poziom_trudnosci']}) "
                "RETURNING id;")
        q = cur.execute(query)
        conn.commit()
        # return redirect(url_for('przepisy.fetch_all_przepisy'))
        query = ("select id from przepis "
              "order by id desc "
              "limit 1;")
        cur.execute(query)
        results = cur.fetchall()
        return redirect(url_for('przepisy.fetch_przepis_with_id', id=results[0][0]))
