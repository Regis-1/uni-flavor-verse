from flask import Flask,jsonify,request, render_template

# creating main Flask app instance
app = Flask(__name__, static_folder='static')
app.json.ensure_ascii = False

# importing blueprints
from routes.przepisy import bp_przepisy
from routes.skladniki import bp_skladniki

app.register_blueprint(bp_przepisy)
app.register_blueprint(bp_skladniki)

@app.route("/")
def home():
    return render_template('base.html')

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)
