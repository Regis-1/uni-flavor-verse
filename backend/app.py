from flask import Flask,jsonify,request

# creating main Flask app instance
app = Flask(__name__)
app.json.ensure_ascii = False

# importing blueprints
from routes.przepisy import bp_przepisy
from routes.uzytkownicy import bp_uzytkownicy
from routes.skladniki import bp_skladniki

app.register_blueprint(bp_przepisy)
app.register_blueprint(bp_uzytkownicy)
app.register_blueprint(bp_skladniki)

@app.route("/")
def home():
    return jsonify({
        "Message": "Witamy REST API flavor-verse - internetowej bazy danych z przepisami kulinarnymi"
        })

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
