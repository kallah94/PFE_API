import datetime
from functions import *
from flask import Flask, request, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from bson import json_util, ObjectId

app = Flask(__name__)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['SECRET_KEY'] = 'secret-key-kallah'
app_context = app.app_context()
app_context.push()
<<<<<<< HEAD
app.config["MONGO_URI"] = "mongodb://localhost:27017/APIBASE"
# app.config["MONGO_URI"] = "mongodb+srv://Amet:amet@clusterprovisionning.3p11m.mongodb.net/vmDatabase?retryWrites=true" \
# "&w=majority"
=======
app.config["MONGO_URI"] = "mongodb://localhost:27017/APIBase"
#app.config["MONGO_URI"] = "mongodb+srv://Amet:amet@clusterprovisionning.3p11m.mongodb.net/vmDatabase?retryWrites=true" \
 #                         "&w=majority"
>>>>>>> cc6d41d62f655ff3eade3fc1477b9cb1c91f65c7
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
    rule = mongo.db.rulesappcloudready.find_one({"name": "rule1"})
    data = setup(project)
    criticity_bound(data["criticity"])
    vector_rule = [rule["complexity"], rule["availability"], rule["criticity"]]
    vector = [data["complexity"], data["availability"], data["criticity"]]
    return {"score": compare_vectors(vector_rule, vector), "providers": ["GCP", "AWS", "AZUR"]}, 200


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

<<<<<<< HEAD
""" GCP CARACTERISTICS"""


@app.route('/gcp', methods=['POST'])
def add_gcp_caracteristics():
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.gcp.insert_one({"fiabilité": fiabilité,
                             "flexibilite": flexibilte,
                             "maturite": maturite,
                             "securite_donnees": securite_donnees,
                             "localisation_geographique": localisation_geographique,
                             "tarification": tarification
                             })
    return 'ok', 200


@app.route('/gcp', methods=['GET'])
def get_gcp_caracteristics():
    gcp_carateristics = mongo.db.gcp.find()
    result = json_util.dumps(gcp_carateristics)
    return result


@app.route('/gcp/<id>', methods=['GET'])
def get_one():
    gcp_caracteristics = mongo.db.gcp.find_one({'_id': ObjectId(id)})
    return gcp_caracteristics


@app.route('/gcp/<id>', methods=['PUT'])
def update_gcp_caracteristics(id):
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.gcp.update_one({'_id': ObjectId(id)}, {'$set': {"fiabilité": fiabilité,
                                                             "flexibilite": flexibilte,
                                                             "maturite": maturite,
                                                             "securite_donnees": securite_donnees,
                                                             "localisation_geographique": localisation_geographique,
                                                             "tarification": tarification
                                                             }
                                                    })
    return 'ok', 200


@app.route('/gcp/<id>', methods=['DELETE'])
def delete_gcp_caracteristics(id):
    mongo.db.gcp.delete_one({'_id': ObjectId(id)})
    return id + 'deleted with success'


""" AZURE CARACTERISTICS"""


@app.route('/azure', methods=['POST'])
def add_azure_caracteristics():
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.azure.insert_one({"fiabilité": fiabilité,
                               "flexibilite": flexibilte,
                               "maturite": maturite,
                               "securite_donnees": securite_donnees,
                               "localisation_geographique": localisation_geographique,
                               "tarification": tarification
                               })
    return 'ok', 200


@app.route('/azure', methods=['GET'])
def get_azure_caracteristics():
    azure_carateristics = mongo.db.azure.find()
    result = json_util.dumps(azure_carateristics)
    return result


@app.route('/azure/<id>', methods=['GET'])
def get_one():
    azure_caracteristics = mongo.db.azure.find_one({'_id': ObjectId(id)})
    return azure_caracteristics


@app.route('/azure/<id>', methods=['PUT'])
def update_azure_caracteristics(id):
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.azure.update_one({'_id': ObjectId(id)}, {'$set': {"fiabilité": fiabilité,
                                                               "flexibilite": flexibilte,
                                                               "maturite": maturite,
                                                               "securite_donnees": securite_donnees,
                                                               "localisation_geographique": localisation_geographique,
                                                               "tarification": tarification
                                                               }
                                                      })
    return 'ok', 200


@app.route('/azure/<id>', methods=['DELETE'])
def delete_azure_caracteristics(id):
    mongo.db.azure.delete_one({'_id': ObjectId(id)})
    return id + 'deleted with success'


""" AMAZONE CARACTERISTICS"""


@app.route('/amazone', methods=['POST'])
def add_amazone_caracteristics():
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.amazone.insert_one({"fiabilité": fiabilité,
                                 "flexibilite": flexibilte,
                                 "maturite": maturite,
                                 "securite_donnees": securite_donnees,
                                 "localisation_geographique": localisation_geographique,
                                 "tarification": tarification
                                 })
    return 'ok', 200


@app.route('/amazone', methods=['GET'])
def get_amazone_caracteristics():
    gcp_carateristics = mongo.db.gcp.find()
    result = json_util.dumps(gcp_carateristics)
    return result


@app.route('/amazone/<id>', methods=['GET'])
def get_one():
    amazone_caracteristics = mongo.db.amazone.find_one({'_id': ObjectId(id)})
    return amazone_caracteristics


@app.route('/amazone/<id>', methods=['PUT'])
def update_amazone_caracteristics(id):
    fiabilité = request.json['fiabilite']
    flexibilte = request.json['flexibilite']
    maturite = request.json['maturite']
    securite_donnees = request.json['data_security']
    localisation_geographique = request.json['localisation_geographique']
    tarification = request.json['tarification']
    mongo.db.amazone.update_one({'_id': ObjectId(id)}, {'$set': {"fiabilité": fiabilité,
                                                                 "flexibilite": flexibilte,
                                                                 "maturite": maturite,
                                                                 "securite_donnees": securite_donnees,
                                                                 "localisation_geographique": localisation_geographique,
                                                                 "tarification": tarification
                                                                 }
                                                        })
    return 'ok', 200


@app.route('/amazone/<id>', methods=['DELETE'])
def delete_amazone_caracteristics(id):
    mongo.db.amazone.delete_one({'_id': ObjectId(id)})
    return id + 'deleted with success'


=======
""" BEGIN CLOUD PROVIDER CRITERIA BEHAVIOR """


@app.route("/providers/criteria", methods=['GET'])
def get_criteria():
    criteria = [doc for doc in mongo.db.criteria.find({})]
    build_criteria_behavior_matrix(criteria)
    return json_util.dumps({'criteria': criteria}), 200


@app.route("/providers/criteria", methods=['POST'])
def set_criterion():
    criteria = json_util.loads(request.data)
    mongo.db.criteria.insert_one(criteria)
    return 'Ok', 200


@app.route("/providers/criteria/<criterion_name>", methods=['PUT'])
def update_criterion(criterion_name):
    new_data = json_util.loads(request.data)
    behavior = new_data['behavior']
    mongo.db.criteria.update_one({"name": criterion_name}, {
        '$set': {
           "behavior": behavior
        }
    })
    return 'Ok', 200


@app.route("/providers/criteria/<criterion_name>", methods=['GET'])
def get_criterion(criterion_name):
    criterion = mongo.db.criteria.find_one({"name": criterion_name})
    return json_util.dumps({'criterion': criterion}), 200


@app.route('/providers/criteria/<criterion_name>', methods=['DELETE'])
def delete_criterion(criterion_name):
    mongo.db.criteria.delete_one({"name": criterion_name})
    return 'ok', 200


>>>>>>> cc6d41d62f655ff3eade3fc1477b9cb1c91f65c7
if __name__ == '__main__':
    app.run()
