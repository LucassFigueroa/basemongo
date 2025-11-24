from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)


# aca nos conectamos a la base de mongodb, si en clase nos toca un pc distinto o asi simplemente cambiamos el localhost
client = MongoClient("mongodb://localhost:27017/")

db = client["tallerbasededatosLSM"]

# las colecciones para que se vean en el navegador 
collection_alumnos = db["alumnos"]
collection_asig = db["asignaturas"]


#CRUD ALUMNOS
@app.route("/")
def home():
    alumnos = list(collection_alumnos.find())
    return render_template("index.html", alumnos=alumnos)

@app.route("/add", methods=["GET", "POST"])
def add_alumno():
    if request.method == "POST":
        collection_alumnos.insert_one({
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"]
        })
        return redirect(url_for("home"))
    return render_template("add_alumno.html")

@app.route("/update/<id>", methods=["GET", "POST"])
def update_alumno(id):
    alumno = collection_alumnos.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        collection_alumnos.update_one(
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
    collection_alumnos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("home"))

# CRUD ASIGNATURAS
@app.route("/asignaturas")
def listar_asignaturas():
    asignaturas = list(collection_asig.find())
    return render_template("asignaturas.html", asignaturas=asignaturas)

@app.route("/asignaturas/add", methods=["GET", "POST"])
def add_asignatura():
    if request.method == "POST":
        collection_asig.insert_one({
            "nombre": request.form["nombre"]
        })
        return redirect(url_for("listar_asignaturas"))
    return render_template("add_asignatura.html")

@app.route("/asignaturas/update/<id>", methods=["GET", "POST"])
def update_asignatura(id):
    asignatura = collection_asig.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        collection_asig.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "nombre": request.form["nombre"]
            }}
        )
        return redirect(url_for("listar_asignaturas"))
    return render_template("update_asignatura.html", asignatura=asignatura)

@app.route("/asignaturas/delete/<id>")
def delete_asignatura(id):
    collection_asig.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("listar_asignaturas"))

if __name__ == "__main__":
    app.run(debug=True)
