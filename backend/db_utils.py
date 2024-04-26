# creating database connection
import psycopg2

conn = psycopg2.connect(
        host="fv-db",
        user="postgres",
        password="my_example")

cur = conn.cursor()

# list of tables' columns with flag if they are not null (necessary)
DatabaseColumns = {
    "Przepis": {
        'autor':True,
        'nazwa':True,
        'opis':False,
        'poziom_trudnosci':True,
        'procedura_wykonania':True,
        'kalorycznosc':False
    },
    "Uzytkownik": {
        'nazwa_uzytkownika':True,
        'haslo':True
    },
    "Skladnik": {
        'nazwa':True
    },
    "Przepis_skladniki": {
        'przepis':True,
        'skladnik':True,
        'ilosc':True,
        'miara':True
    }
}


def extract_table_fields(json_data, tablename, create=True):
    result = {}
    for k, v in DatabaseColumns[tablename].items():
        gotValue = json_data.get(k)
        if (not gotValue):
            if create and v:
                return None
        else:
            result[k] = gotValue

    # changing number values to integers and adding '' to strings
    for k, v in result.items():
        try:
            int(v)
            result[k] = str(v)
        except Exception as e:
            result[k] = f"'{v}'"

    return result


def create_from_json(json_data, tablename):
    if not json_data:
        return "Błędny format JSON!"
    if not tablename:
        return "Brak wybranej tabeli."

    fields = extract_table_fields(json_data, tablename)
    if not fields:
        return f"Brak wymaganych pól by dodać {tablename}."

    headers = 'insert into ' + tablename + '(' + ','.join(list(fields.keys())) + ') '
    values = 'values (' + ','.join([v for v in list(fields.values())]) + ');'
    query = headers + values
    
    cur.execute(query)
    conn.commit()
    return f"{tablename} został poprawnie dodany."


def update_from_json(json_data, tablename, condition):
    if not json_data:
        return "Błędny format JSON!"

    fields = extract_table_fields(json_data, tablename, False)
    if len(fields) < 1:
        return "Brak sensownych pól do aktualizacji."

    # update table set col1 = 'hello' where condition;
    update_cols = ','.join([f"{v[0]}={v[1]}" for v in fields.items()])
    query = f"update {tablename} set {update_cols} where {condition};"

    cur.execute(query)
    conn.commit()
    return "Przepis został poprawnie zaktualizowany."


def read_columns_from_table(table, columns, filter=None, select_one=False):
    columns_together = ','.join(columns)
    query = f"select {columns_together} from {table}"

    if filter:
        query += f" where {filter}"
    query += ";"

    cur.execute(query)
    result = cur.fetchone() if select_one else cur.fetchall()
    return result


def delete_record_from_table(table, condition):
    query = f'delete from {table} where {condition};'
    cur.execute(query)
    conn.commit()
