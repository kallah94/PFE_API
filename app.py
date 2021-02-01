import datetime

from flask import Flask, json, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from functions import *

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_envvar('ENV_FILE_LOCATION')
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
    hash_password = bcrypt.generate_password_hash(str(password))
    sql = "INSERT INTO users(username, password) VALUES (%s, %s)"
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (username, hash_password))
    mysql.connection.commit()
    return 'ok'


@app.route('/criteres', methods=['GET'])
def get_criteres():
    sql = 'SELECT * FROM criteres WHERE 1=1'
    cursor = mysql.connection.cursor()
    cursor.execute(sql)
    criteres = cursor.fetchall()
    fields_list = cursor.description
    mysql.connection.commit()
    cursor.close()
    data = jsonify({'criteres': cust_jsonify(fields_list, criteres)})
    return data


@app.route('/criteres', methods=['POST'])
def set_critere():
    data = json.loads(request.data)
    name = data['name']
    vlrate = data['vlrate']
    lrate = data['lrate']
    mrate = data['mrate']
    hrate = data['hrate']
    vhrate = data['vhrate']
    print(type(vhrate))
    sql = "INSERT INTO criteres(name, vlrate, lrate, mrate, hrate, vhrate) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = mysql.connection.cursor()
    cursor.execute(sql, (name, vlrate, lrate, mrate, hrate, vhrate))
    mysql.connection.commit()
    return 'ok'


@app.route('/get_token', methods=['GET'])
def get_user_data():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    sql = "SELECT * FROM users WHERE username=%s"
    cursor = mysql.connect.cursor()
    cursor.execute(sql, (username,))
    mysql.connection.commit()
    user = cursor.fetchone()
    authorized = bcrypt.check_password_hash(user[2], str(password))
    if not authorized:
        return {'error': 'username or password invalid'}, 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user[0]), expires_delta=expires)
    return {'token': access_token}, 200


if __name__ == '__main__':
    app.run(debug=True)
