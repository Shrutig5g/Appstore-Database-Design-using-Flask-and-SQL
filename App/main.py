from flask import Flask, render_template
import urllib.request, json,pyodbc
cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=testDb;Trusted_Connection=yes;timeout=5000')
cursor = cnxn.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)