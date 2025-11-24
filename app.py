from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Conexión a MongoDB (ajusta si tu puerto o host son distintos)
client = MongoClient("mongodb://localhost:27017/")
db = client["taller_basededatos"]   # Nombre de la base de datos
collection = db["alumnos"]          # Colección sobre la que haremos CRUD

@app.route("/")
def home():
    alumnos = list(collection.find())
    return render_template("index.html", alumnos=alumnos)

@app.route("/add", methods=["GET", "POST"])
def add_alumno():
    if request.method == "POST":
        collection.insert_one({
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"]
        })
        return redirect(url_for("home"))
    return render_template("add_alumno.html")

@app.route("/update/<id>", methods=["GET", "POST"])
def update_alumno(id):
    alumno = collection.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"],
                "apellido": request.form["apellido"]
            }}
        )
        return redirect(url_for("home"))
    return render_template("update_alumno.html", alumno=alumno)

@app.route("/delete/<id>")
def delete_alumno(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
