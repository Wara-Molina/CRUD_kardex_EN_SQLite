#
# Flask: 
# render_template: para las plantillas
# request: para peticiones
# redirect: respuestas que se generaran
# url_for: referenciar a las url atravez de las funciones

from flask import Flask,render_template,request,redirect,url_for
import sqlite3 

app = Flask(__name__)
# Creacion de base de datos y tablas
# funcion
def init_database():
    # se crea la dase de datos en caso de que no exista
    #  si existe la bd se conecta a la base de datos
    conn = sqlite3.connect("kardex.db")
    # cursor: nos sirve para hacer insercion, eliminacion, modificacion etc. de sentencias sql
    cursor = conn.cursor()
    cursor.execute(
        #  fecha: YYYY-mm-dd
        """
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha_nac TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/personas")
def personas():
    conn = sqlite3.connect("kardex.db")
    # Permite manejar los registros como diccionarios
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    personas = cursor.fetchall()
    return render_template("personas/index.html",personas = personas)

@app.route("/personas/create")
def create():
    return render_template('personas/create.html')

@app.route("/personas/create/save",methods=['POST'])
def personas_save():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    fecha_nac = request.form['fecha_nac']
    
    conn = sqlite3.connect("kardex.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO personas (nombre,telefono,fecha_nac) VALUES (?,?,?)",(nombre, telefono, fecha_nac))
    
    conn.commit()
    conn.close()
    return redirect('/personas')
    



if __name__=="__main__":
    app.run(debug=True)
     