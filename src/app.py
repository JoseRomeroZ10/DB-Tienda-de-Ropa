from flask import Flask, render_template, request , redirect, url_for
import os
import database as db

templates_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

templates_dir = os.path.join(templates_dir, 'src', 'templades')

app = Flask(__name__, template_folder = "templates")

#rutas del la aplicacion
@app.route('/')
def home():

    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    #Convertir los datos a Diccionario 
    insertObject = []
    columnNames = [column[0] for column in  cursor.description]
    for record in myresult:
        insertObject .append(dict(zip(columnNames, record )))
    cursor.close()
    

    return render_template('index.html', data = insertObject)

@app.route("/clientes",methods = ["POST","GET"])
def post():
    if request.method == "POST":

        Nombre_Cliente = request.form['Name']
        Apellido_Cliente = request.form['Apellido']
        Email_Cliente = request.form['Email_Cliente']
        Telefono_Cliente = request.form['Email']

    if Nombre_Cliente and Apellido_Cliente and Email_Cliente and Telefono_Cliente:
        cursor  =db.database.cursor()
        sql = "INSERT INTO clientes (Nombre_Cliente, Apellido_Cliente, Email_Cliente, Telefono_Cliente) VALUES (%s, %s, %s, %s)"
        data = (Nombre_Cliente, Apellido_Cliente, Email_Cliente, Telefono_Cliente)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:ID_Cliente>')
def delete(ID_Cliente):
    
    cursor  =db.database.cursor()
    sql = " DELETE FROM clientes WHERE ID_Cliente=%s "
    data = (ID_Cliente,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:ID_Cliente>', methods = ['POST'])
def edit(ID_Cliente):
    Nombre_Cliente = request.form['Name']
    Apellido_Cliente = request.form['Apellido']
    Email_Cliente = request.form['Email_Cliente']
    Telefono_Cliente = request.form['Email']


    cursor  =db.database.cursor()
    sql = " UPDATE clientes SET Nombre_Cliente = %s, Apellido_Cliente = %s, Email_Cliente = %s, Telefono_Cliente = %s WHERE ID_Cliente=%s "
    data = (Nombre_Cliente, Apellido_Cliente, Email_Cliente, Telefono_Cliente,ID_Cliente)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port = 4000)

