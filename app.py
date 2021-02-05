from flask import Flask, render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql Connection
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='8452'
app.config['MYSQL_DB']='codyd'

#Seccion settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)
###############################################
#          Render Home page                   #
###############################################
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('Select * From users')
    data = cur.fetchall()

    return render_template('index.html', users = data)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        fullname = request.form['fullname']
        age = request.form['age']
        num_children = request.form['num_children']
        car=request.form['question-Car']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (Nombre, Apellido, Edad, Num_Hijos,Vehiculo) VALUES(%s, %s, %s, %s,%s)',(name,fullname,age,num_children,car))
        mysql.connection.commit()
        flash('Usuario agregado Correctamente')
        # print(name+fullname+age)        
    return redirect(url_for('Index'))

@app.route('/edit_user/<id>')
def get_user(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = {0}'.format(id))
    data = cur.fetchall()
    
    return render_template('edit-user.html', user=data[0])

@app.route('/update/<id>',methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        fullname = request.form['fullname']
        age = request.form['age']
        num_children = request.form['num_children']
        car=request.form['question-Car']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET Nombre = %s,
                Apellido =%s,
                Edad = %s,
                Num_Hijos = %s,
                Vehiculo= %s
            WHERE id = %s
        """,(name,fullname,age,num_children,car,id))
        mysql.connection.commit()    
        flash('Usuario Editado Correctamente')
    return redirect(url_for('Index'))

@app.route('/delete_user/<string:id>')
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = {0}'.format(id))
    mysql.connection.commit()    
    flash('Usuario Eliminado Correctamente')
    return redirect(url_for('Index'))

###############################################
#          Render Buy page                   #
###############################################
@app.route('/compras',methods=["GET"])
def Compras():
     return render_template('compras.html')
    
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Id FROM users ')
    data = cur.fetchall()
    print(data)
    return 

@app.route('/buy',methods=['POST'])
def buy():
    if request.method == 'POST':
        id = request.form['Id']
        product = request.form['product']
        

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO compras(Fecha_Compra,Id_User,Product) VALUES(NOW(),%s,%s)',(id,product))
        mysql.connection.commit()    
        flash('Compra Saticfactoria')
    return redirect(url_for('Compras'))



if  __name__ == '__main__':
    app.run(port = 3000, debug=True )