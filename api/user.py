import pymysql
import mysql.connector
from mysql.connector import Error
from flask import Flask,jsonify,request,json,redirect,render_template

# connection = pymysql.connect(host="localhost",
#     user="root",
#     password="9695948586",
#     database="gb")



try:
    connection = mysql.connector.connect(host="localhost",
    user="root",
    password="9695948586",
    database="gb"
    )
    print("MySQL Database connection successful")
except Error as err:
    print(f"Error: '{err}'")

cursor = connection.cursor()
 


app = Flask(__name__)

@app.route('/')
def api_root():
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM gb.clentes;")
  rows = cursor.fetchall()
  print(rows, enumerate(rows))
  result = {}
  for i, row in enumerate(rows):
      result[i] = {}
      for j, col in enumerate(cursor.description):
          col_name = col[0]
          result[i][col_name] = row[j]
  print(result)
  return jsonify(result)


@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        nome = request.form['nome']
        print(nome)
        valor = request.form['valor']
        cursor.execute(f'INSERT INTO gb.clentes (nome, valor) VALUES ("{nome}","{valor}")')
        connection.commit()
        return redirect('/')
    else:
        return render_template('form.html')

@app.route('/<int:id>')
def mostra_um(id):
  cursor.execute(f'SELECT * FROM gb.clentes WHERE idclentes = {id};')
  dado =cursor.fetchall()
  print(dado)
  return jsonify(dado)

@app.route('/deletar/<int:id>')
def deletar_id(id):
  cursor.execute(f'DELETE from gb.clentes WHERE idclentes = {id};')
  connection.commit()
  return redirect('/')

@app.route('/deletar',methods=['GET', 'POST'])
def delete():
  if request.method == 'POST':
    id = request.form['idclentes']
    cursor.execute(f'DELETE from gb.clentes WHERE idclentes = {id};')
    connection.commit()
    return redirect('/')
  else:
    return render_template('del.html')




if __name__ == '__main__':
  app.run(debug=True)
