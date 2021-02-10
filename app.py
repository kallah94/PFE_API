import datetime
from functions import *
from flask import Flask, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['SECRET_KEY'] = 'secret-key-kallah'
app_context = app.app_context()
app_context.push()
# app.config["MONGO_URI"] = "mongodb://localhost:27017/APIBase"
app.config["MONGO_URI"] = "mongodb+srv://Amet:amet@clusterprovisionning.3p11m.mongodb.net/vmDatabase?retryWrites=true" \
                          "&w=majority"
mongo = PyMongo(app)


@app.route('/')
def hello():
    return {"hello": "Hello world !!!"}


@app.route('/register', methods=['POST'])
def register():
    user_data = json_util.loads(request.data)
    username = user_data['username']
    password = user_data['password']
    hashed_password = Bcrypt.generate_password_hash(Bcrypt, password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})
    return 'ok', 200


@app.route('/login', methods=['POST'])
def login():
    data = json_util.loads(request.data)
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
    user_data = [doc for doc in mongo.db.users.find({})]
    return json_util.dumps({"users": user_data}), 200


""" BEGIN CRITERES CRUD SECTION """


@app.route('/criteres', methods=['GET'])
# @jwt_required
def get_criteres():
    data = [doc for doc in mongo.db.criteres.find({})]
    return json_util.dumps({"criteres": data}), 200


@app.route('/criteres', methods=['POST'])
# @jwt_required
def set_critere():
    data = json_util.loads(request.data)
    print(data)
    mongo.db.criteres.insert_one(data)
    return 'Ok', 200


@app.route('/criteres/<name>', methods=['GET'])
def get_critere(name):
    critere = mongo.db.criteres.find_one({"name": name})
    return json_util.dumps({"critere": critere}), 200


@app.route('/criteres/<name>', methods=['PUT'])
def update_critere(name):
    new_data = json_util.loads(request.data)
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
    data = json_util.loads(request.data)
    print(data)
    mongo.db.rulesappcloudready.insert_one(data)
    return 'ok', 200


@app.route('/rulesappcloudready', methods=['GET'])
def get_rulesappcloudreay():
    data = [doc for doc in mongo.db.rulesappcloudready.find({})]
    return json_util.dumps({"rulesappcloudready": data}), 200


@app.route('/rulesappcloudready/<name>', methods=['GET'])
def get_rule(name):
    rule_data = mongo.db.rulesappcloudready.find_one({"name": name})
    return json_util.dumps({"ruleappcloudready": rule_data}), 200


@app.route('/rulesappcloudready/<name>', methods=['PUT'])
def update_rule(name):
    new_data = json_util.loads(request.data)
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


""" END RULESAPPCLOUDREADY SECTION """

""" BEGIN PROJECT CRUD """


@app.route('/projects', methods=['GET'])
def get_projects():
    projects = [doc for doc in mongo.db.projects.find({})]
    return json_util.dumps({'projects': projects}), 200


@app.route('/projects/<project_name>', methods=['GET'])
def get_project(project_name):
    project = mongo.db.projects.find_one({"projectName": project_name})
    project = json_util.dumps({'project': project})
    return project, 200

"""
@app.route('/projects', methods=['POST'])
def set_project():
    data = request.data
    project_form = json_util.loads(data)
    try:
        mongo.db.projects.insert_one(project_form)
        return redirect(url_for('.conseil', project=data))
    except:
        return {"error": "An error occurr project can't be store to the database"}, 500
"""


@app.route('/projects', methods=['POST'])
def conseil():
    project = json_util.loads(request.data)
    print(project["applicationType"])
    rule = mongo.db.rulesappcloudready.find_one({"name": "rule1"})
    data = setup(project)
    vector_rule = [rule["complexity"], rule["availability"], rule["criticity"]]
    vector = [data["complexity"], data["availability"], data["criticity"]]

    return {"score": compare_vectors(vector_rule, vector), "Providers": ["GCP", "AWS", "AZUR"]}, 200


@app.route('/projects/<name>', methods=['PUT'])
def update_project(name):
    new_data = json_util.loads(request.data)
    application_type = new_data["applicationType"]
    dependencies = new_data["dependencies"]
    sla = new_data["SLA"]
    environment = new_data["environment"]
    data_size = new_data["dataSize"]
    connected_applications = new_data["connectedApplications"]
    tech_requirements = new_data["techRequirements"]
    cost_estimation = new_data["costEstimation"]
    cpu = new_data["cpu"]
    disk = new_data["disk"]
    memory = new_data["memory"]
    number_of_vm = new_data["numberOfVm"]
    os_image = new_data["osImage"]
    os_type = new_data["osType"]
    mongo.db.projects.update_one({"projectName": name}, {
        '$set': {
            "applicationType": application_type, "dependencies": dependencies,
            "SLA": sla, "environment": environment, "dataSize": data_size,
            "connectedApplications": connected_applications,
            "techRequirements": tech_requirements, "costEstimation": cost_estimation,
            "cpu": cpu, "disk": disk, "memory": memory, "numberOfVm": number_of_vm,
            "osImage": os_image, "osType": os_type
        }
    })
    return 'ok', 200


@app.route('/projects/<project_name>', methods=['DELETE'])
def delete_project(project_name):
    mongo.db.projects.delete_one({"projectName": project_name})
    return 'ok', 200


""" END PROJECT CRUD"""

if __name__ == '__main__':
    app.run()
