from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tbmedicos'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tb_medicos')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tb_medicos: {e}")
        flash('Error al realizar la consulta.')
        return render_template('index.html', albums=[])

@app.route('/registro', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        try:
            Fnombre = request.form['txtNombre']
            Frfc = request.form['txtRfc']
            Fcedula = request.form['txtCedula']
            Fcorreo = request.form['txtCorreo']
            Fcontraseña = request.form['txtContraseña']
            Frol = request.form['txtRol']
            
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO tbmedicos (nombre, rfc, cedulaP, correoE, contraseña, rol) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (Fnombre, Frfc, Fcedula, Fcorreo, Fcontraseña, Frol))
            mysql.connection.commit()
            flash('Médico registrado correctamente')
            return redirect(url_for('consultas')) 
        except Exception as e:
            print(f"Error al registrar el médico: {e}")
            flash('Error al registrar el médico: ' + str(e))
            return redirect(url_for('formulario'))  
    
    return render_template('GuardarAlbum.html')

@app.route('/consultas')
def consultas():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM tbmedicos')
        consultaA = cursor.fetchall()
        return render_template('consultaMedicos.html', view='ConsultaMedicos', medicos=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tbmedicos: {e}")
        return render_template('consultaMedicos.html', view='ConsultaMedicos', medicos=[])

@app.route('/editar/<id>')
def editar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM tbmedicos WHERE id=%s', [id])
        consultaA = cur.fetchone()
        return render_template('editar.html', medicos=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tbmedicos: {e}")
        flash('Error al consultar el médico: ' + str(e))
        return redirect(url_for('home'))

@app.route('/ActualizarAlbum/<id>', methods=['POST'])
def ActualizarAlbum(id):
    if request.method == 'POST':
        try:
            Fnombre = request.form['txtNombre']
            Frfc = request.form['txtRfc']
            Fcedula = request.form['txtCedula']
            Fcorreo = request.form['txtCorreo']
            Fcontraseña = request.form['txtContraseña']
            Frol = request.form['txtRol']

            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE tbmedicos SET nombre=%s, rfc=%s, cedulaP=%s, correoE=%s, contraseña=%s, rol=%s WHERE id=%s',
                           (Fnombre, Frfc, Fcedula, Fcorreo, Fcontraseña, Frol, id))
            mysql.connection.commit()
            flash('Médico actualizado correctamente')
            return redirect(url_for('home'))

        except Exception as e:
            flash('Error al actualizar el médico: ' + str(e))
            print(e)
            return redirect(url_for('home'))

@app.route('/eliminar/<id>')
def eliminar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM tbmedicos WHERE id=%s', [id])
        mysql.connection.commit()
        flash('Se ha eliminado correctamente')
        return redirect(url_for('home'))
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
        return redirect(url_for('home'))

@app.route('/expediente')
def expediente():
    return render_template('expediente.html')

@app.route('/registroP', methods=['GET', 'POST'])
def registroP():
    if request.method == 'POST':
        try:
            Fmedico = request.form['txtMedico']
            Fnombre = request.form['txtNombre']
            Ffecha_nac = request.form['txtfecha_nac']
            Fenfermedades_cronicas = request.form['txtenfermedades_cronicas']
            Falergias = request.form['txtalergias']
            Fantecedentes_familiares = request.form['txtantecedentes_familiares']
            
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO pacientes (medico, nombre, fecha_nac, enfermedades_cronicas, alergias, antecedentes_familiares) VALUES (%s, %s, %s, %s, %s, %s)', 
                           (Fmedico, Fnombre, Ffecha_nac, Fenfermedades_cronicas, Falergias, Fantecedentes_familiares))
            mysql.connection.commit()
            flash('Paciente registrado correctamente')
            return redirect(url_for('expediente')) 
        except Exception as e:
            print(f"Error al registrar al paciente: {e}")
            flash('Error al registrar al paciente: ' + str(e))
            return redirect(url_for('expediente'))  
    
    return render_template('guardarpacientes.html')

@app.route('/exploracion')
def exploracion():
    return render_template('exploracion.html')

@app.route('/diagnostico')
def diagnostico():
    return render_template('diagnostico.html')

@app.route('/consultarPacientes')
def consultaP():
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM pacientes')
            consultaA = cursor.fetchall()
            return render_template('consultaP.html', view='consultaP', pacientes=consultaA)
        except Exception as e:
            print(f"Error al realizar la consulta en la tabla tbmedicos: {e}")
            return render_template('consultaP.html', view='consultaP', pacientes=[])
    
@app.route('/editarP/<id>')
def editarP(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pacientes WHERE id=%s', [id])
        consultaA = cur.fetchone()
        return render_template('editarP.html', pacientes=consultaA)
    except Exception as e:
        print(f"Error al realizar la consulta en la tabla tbmedicos: {e}")
        flash('Error al consultar el médico: ' + str(e))
        return redirect(url_for('expediente'))

@app.route('/ActualizarP/<id>', methods=['POST'])
def ActualizarP(id):
    if request.method == 'POST':
        try:
            Fmedico = request.form['txtMedico']
            Fnombre = request.form['txtNombre']
            Ffecha_nac = request.form['txtfecha_nac']
            Fenfermedades_cronicas = request.form['txtenfermedades_cronicas']
            Falergias = request.form['txtalergias']
            Fantecedentes_familiares = request.form['txtantecedentes_familiares']

            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE pacientes SET medico=%s, nombre=%s, fecha_nac=%s, enfermedades_cronicas=%s, alergias=%s, antecedentes_familiares=%s WHERE id=%s', 
                           (Fmedico, Fnombre, Ffecha_nac, Fenfermedades_cronicas, Falergias, Fantecedentes_familiares, id))
            
            mysql.connection.commit()
            flash('Médico actualizado correctamente')
            return redirect(url_for('expediente'))

        except Exception as e:
            flash('Error al actualizar el médico: ' + str(e))
            print(e)
            return redirect(url_for('expediente'))

@app.errorhandler(404)
def paginando(e):
    return 'Sintaxis incorrecta', 404

if __name__ == '__main__':
    app.run(port=9000, debug=True)
