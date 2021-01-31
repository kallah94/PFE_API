from flask import Flask, json, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-kallah'
app_context = app.app_context()
app_context.push()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kallah'
app.config['MYSQL_PASSWORD'] = 'kallah'
app.config['MYSQL_DB'] = 'testdb'
mysql = MySQL(app)


@app.route('/')
def hello_world():
    return ' hello world'


@app.route('/users', methods=['GET'])
def get_users():
    sql = 'SELECT * FROM users WHERE 1=1'
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    users = cursor.fetchall()
    fields_list = cursor.description
    mysql.connection.commit()
    cursor.close()
    data = jsonify({'users': cust_jsonify(fields_list, users)})
    return data


@app.route('/users', methods=['POST'])
def set_user():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    hash_password = generate_password_hash(password)
    sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
    cursor = mysql.connection.cursor()
    print(hash_password)
    cursor.execute(sql, (username, hash_password))
    mysql.connection.commit()
    return 'ok'


@app.route('/get/criteres', methods=['GET'])
def get_criteres():
    sql = 'SELECT * FROM criteres WHERE 1=1'
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    criteres = cursor.fetchall()
    fields_list = cursor.description
    mysql.connection.commit()


if __name__ == '__main__':
    app.run(debug=True)
