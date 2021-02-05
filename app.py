import datetime
from functions import *
from flask import Flask, json, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['SECRET_KEY'] = 'secret-key-kallah'
app_context = app.app_context()
app_context.push()
app.config["MONGO_URI"] = "mongodb://localhost:27017/APIBase"
mongo = PyMongo(app)


@app.route('/register', methods=['POST'])
def register():
    user_data = json.loads(request.data)
    username = user_data['username']
    password = user_data['password']
    hashed_password = Bcrypt.generate_password_hash(Bcrypt, password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    username = data['username']
    password = data['password']
    hashed = mongo.db.users.find_one({"username": username})['password']
    authorized = bcrypt.check_password_hash(hashed, str(password))
    if not authorized:
        return {'error': 'username or password invalid'}, 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(password), expires_delta=expires)
    return {'token': access_token}, 200


@app.route('/users', methods=['GET'])
def get_users():
    user_data = list(mongo.db.users.find())
    user_data = json.dumps(user_data, default=newEncoder)
    return user_data, 200


""" BEGIN CRITERES CRUD SECTION """


@app.route('/criteres', methods=['GET'])
# @jwt_required
def get_criteres():
    data = list(mongo.db.criteres.find())
    data = json.dumps(data, default=newEncoder)
    return data, 200


@app.route('/criteres', methods=['POST'])
# @jwt_required
def set_critere():
    data = json.loads(request.data)
    print(data)
    mongo.db.criteres.insert_one(data)
    return 'Ok', 200


@app.route('/criteres/<name>', methods=['GET'])
def get_critere(name):
    critere = mongo.db.criteres.find_one({"name": name})
    critere = json.dumps(critere, default=newEncoder)
    return critere, 200


@app.route('/criteres/<name>', methods=['PUT'])
def update_critere(name):
    new_data = json.loads(request.data)
    vlrate = new_data["vlrate"]
    lrate = new_data["lrate"]
    mrate = new_data["mrate"]
    hrate = new_data["hrate"]
    vhrate = new_data["vhrate"]
    mongo.db.criteres.update_one({"name": name},
                                 {'$set': {"vlrate": vlrate, "lrate": lrate,
                                           "mrate": mrate, "hrate": hrate, "vhrate": vhrate}})
    return 'ok'


@app.route('/criteres/<name>', methods=['DELETE'])
def delete_critere(name):
    mongo.db.criteres.delete_one({"name": name})
    return 'ok', 200


""" END CRITERES CRUD SECTION """

""" BEGIN RULESAPPCLOUDREADY SECTION """


@app.route('/rulesappcloudready', methods=['POST'])
def set_ruleappcloudready():
    data = json.loads(request.data)
    print(data)
    mongo.db.rulesappcloudready.insert_one(data)
    return 'ok', 200


@app.route('/rulesappcloudready', methods=['GET'])
def get_rulesappcloudreay():
    data = list(mongo.db.rulesappcloudready.find())
    data = json.dumps(data, default=newEncoder)
    return data, 200


@app.route('/rulesappcloudready/<name>', methods=['GET'])
def get_rule(name):
    rule_data = mongo.db.rulesappcloudready.find_one({"name": name})
    rule_data = json.dumps(rule_data, default=newEncoder)
    return rule_data, 200


@app.route('/rulesappcloudready/<name>', methods=['PUT'])
def update_rule(name):
    new_data = json.loads(request.data)
    print(new_data)
    complexity = new_data["complexity"]
    availability = new_data["availability"]
    criticity = new_data["criticity"]
    mongo.db.rulesappcloudready.update_one({"name": name},
                                           {'$set': {"complexity": complexity,
                                                     "availability": availability, "criticity": criticity}})
    return 'ok', 200


@app.route('/rulesappcloudready/<name>', methods=['DELETE'])
def delete_rule(name):
    mongo.db.rulesappcloudready.delete_one({"name": name})
    return 'Ok', 200


""" END RULESAPPCLOUDREADY SECTION"""

""" BEGIN PROJECT CRUD """


@app.route('/projects', methods=['GET'])
def get_projects():
    projects = mongo.db.projects.find()
    projects = json.dumps(projects, default=newEncoder)
    return projects, 200


@app.route('/projects/<project_name>', methods=['GET'])
def get_project(project_name):
    project = mongo.db.projects.find_one({"projectName": project_name})
    project = json.dumps(project, default=newEncoder)
    return project, 200


@app.route('/projects', methods=['POST'])
def set_project():
    project_form = json.loads(request.data)
    mongo.db.projects.insert_one(project_form)
    return 'ok', 200


@app.route('/projects/<project_name>', methods=['PUT'])
def update_project(project_name):
    mongo.db.projects.update_one({"projectName": project_name}, {
        '$set': {}
    })
    return 'ok', 200


@app.route('/projects/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    mongo.db.projects.delete_one({"projectName": project_name})
    return 'ok', 200


""" END PROJECT CRUD"""

if __name__ == '__main__':
    app.run()
