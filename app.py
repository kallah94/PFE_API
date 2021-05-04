import datetime

from bson import json_util

from functions import *
from flask import Flask, request, render_template_string, make_response, jsonify
from flask_jwt_extended import *
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['SECRET_KEY'] = 'secret-key-kallah'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "kallahbenakhmeth@gmail.com"
app.config['MAIL_PASSWORD'] = "kFceNE35b34Z4yK"
mail = Mail(app)

app_context = app.app_context()
app_context.push()
app.config["MONGO_URI"] = "mongodb://localhost:27017/APIBase"

# app.config["MONGO_URI"] = "mongodb+srv://Amet:amet@clusterprovisionning.3p11m.mongodb.net/vmDatabase?retryWrites=true"\
#                          "&w=majority"

mongo = PyMongo(app)


@app.route('/register', methods=['POST'])
def register():
    user_data = json_util.loads(request.data)
    username = user_data['username']
    password = user_data['password']
    email = user_data['email']
    hashed_password = Bcrypt.generate_password_hash(Bcrypt, password)
    mongo.db.users.insert_one({"username": username, "email": email, "password": hashed_password})
    return {
               'message': 'user created successfully'
           }, 200


@app.route('/login', methods=['POST'])
def login():
    data = json_util.loads(request.data)
    username = data['username']
    password = data['password']
    try:
        hashed = mongo.db.users.find_one({"username": username})['password']
        authorized = bcrypt.check_password_hash(hashed, str(password))
        if not authorized:
            return {'error': 'username or password invalid'}, 401
        expires = datetime.timedelta(days=7)
        access_token, refresh_token = create_access_token(identity=username, expires_delta=expires), \
                                      create_refresh_token(identity=username)
        return {
                   'accesToken': access_token,
                   "refreshToken": refresh_token
               }, 200
    except:
        return {
                   'message': "User with this credentials not found please check username/password."
               }, 404


@app.route('/send-reset-token', methods=['POST'])
def send_reset_token():
    data = json_util.loads(request.data)
    email = data['email']
    user = mongo.db.users.find_one({'email': email})
    if user:
        expires = datetime.timedelta(minutes=15)
        reset_token = create_access_token(identity=email, expires_delta=expires)
        msg = Message()
        msg.subject = "Mail de recuperation de password "
        msg.recipients = [email]
        msg.sender = 'kallahbenakhmeth@gmail.com'
        msg.body = 'Reset Password'
        msg.html = render_template_string('<h4>Ce mail est valid durant 15 minutes </h4>\
        <a href=http://localhost:4200/reset-password/{{token}}> Link to reset '
                                          'password </a>', token=reset_token)
        mail.send(msg)
        return {'resetPasswordToken': reset_token}, 200
    else:
        return 'Error Email not found', 404


@app.route('/reset-password/<token>', methods=['POST'])
def reset_password_with_token(token):
    data = json_util.loads(request.data)
    email = decode_token(token)['identity']
    user = mongo.db.users.find_one({'email': email})
    if user:
        password = data['password']
        print(password)
        hashed_password = Bcrypt.generate_password_hash(Bcrypt, password)
        mongo.db.users.update({'username': user['username'], 'email': email},
                              {'$set': {
                                  'password': hashed_password
                              }})
        response = make_response(
            jsonify(
                {'message': 'password change successfully !!'}
            ),
            200
        )
        response.headers['Content-Type'] = "application/json"
    return response
    return 'Error User with this email not found', 404


""" BEGIN CRITERES CRUD SECTION """


@app.route('/criteres', methods=['GET'])
@jwt_required
def get_criteres():
    print(request.data)
    data = [doc for doc in mongo.db.criteres.find({})]
    return json_util.dumps({"criteres": data}), 200


@app.route('/criteres', methods=['POST'])
@jwt_required
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
@jwt_required
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
@jwt_required
def delete_critere(name):
    mongo.db.criteres.delete_one({"name": name})
    return 'ok', 200


""" END CRITERES CRUD SECTION """

""" BEGIN RULESAPPCLOUDREADY SECTION """


@app.route('/rulesappcloudready', methods=['POST'])
@jwt_required
def set_ruleappcloudready():
    data = json_util.loads(request.data)
    print(data)
    mongo.db.rulesappcloudready.insert_one(data)
    return 'ok', 200


@app.route('/rulesappcloudready', methods=['GET'])
@jwt_required
def get_rulesappcloudreay():
    data = [doc for doc in mongo.db.rulesappcloudready.find({})]
    return json_util.dumps({"rulesappcloudready": data}), 200


@app.route('/rulesappcloudready/<name>', methods=['GET'])
@jwt_required
def get_rule(name):
    rule_data = mongo.db.rulesappcloudready.find_one({"name": name})
    return json_util.dumps({"ruleappcloudready": rule_data}), 200


@app.route('/rulesappcloudready/<name>', methods=['PUT'])
@jwt_required
def update_rule(name):
    new_data = json_util.loads(request.data)
    complexity = new_data["complexity"]
    availability = new_data["availability"]
    criticity = new_data["criticity"]
    type = new_data["type"]
    mongo.db.rulesappcloudready.update_one({"name": name},
                                           {'$set': {"complexity": complexity,
                                                     "availability": availability,
                                                     "criticity": criticity,
                                                     "type": type}
                                            }
                                           )
    return 'ok', 200


@app.route('/rulesappcloudready/<name>', methods=['DELETE'])
@jwt_required
def delete_rule(name):
    mongo.db.rulesappcloudready.delete_one({"name": name})
    return 'Ok', 200


""" END RULESAPPCLOUDREADY SECTION """

""" BEGIN PROJECT CRUD """


@app.route('/projects', methods=['GET'])
@jwt_required
def get_projects():
    projects = [doc for doc in mongo.db.projects.find({})]
    return json_util.dumps({'projects': projects}), 200


@app.route('/projects/<project_name>', methods=['GET'])
@jwt_required
def get_project(project_name):
    project = mongo.db.projects.find_one({"projectName": project_name})
    project = json_util.dumps({'project': project})
    return project, 200


@app.route('/projects', methods=['POST'])
@jwt_required
def conseil():
    project = json_util.loads(request.data)
    data = setup(project)
    print(data)
    rule = mongo.db.rulesappcloudready.find_one({"type": data["application_type"]})
    vector_rule = [rule["complexity"], rule["availability"], rule["criticity"]]
    vector = [data["complexity"], data["availability"], data["criticity"]]
    providers = [doc for doc in mongo.db.providers.find({})]

    criteria = [doc for doc in mongo.db.criteria.find({})]
    categories = [doc for doc in mongo.db.pricing.find({"cpu": data["cpu"], "ram": data["ram"]})]
    app_readyness(vector_rule, vector, data["criticity"], categories)
    print(providers)
    build_criteria_behavior_matrix(criteria)
    providers = make_provider_list(providers, criteria)
    return {"score": compare_vectors(vector_rule, vector), "providers": providers}, 200


@app.route('/projects/<name>', methods=['PUT'])
@jwt_required
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
@jwt_required
def delete_project(project_name):
    mongo.db.projects.delete_one({"projectName": project_name})
    return 'ok', 200


""" END PROJECT CRUD"""

""" BEGIN CLOUD PROVIDER CRITERIA BEHAVIOR """


@app.route("/providers/criteria", methods=['GET'])
@jwt_required
def get_criteria():
    criteria = [doc for doc in mongo.db.criteria.find({})]
    build_criteria_behavior_matrix(criteria)
    return json_util.dumps({'criteria': criteria}), 200


@app.route("/providers/criteria", methods=['POST'])
@jwt_required
def set_criterion():
    criteria = json_util.loads(request.data)
    mongo.db.criteria.insert_one(criteria)
    percentage_update()
    return 'Ok', 200


def percentage_update():
    result = mongo.db.criteria.aggregate([{
        '$group': {
            '_id': 'null',
            'totalSum': {
                '$sum': "$weight"
            }
        }
    }])
    total_sum = list(result)[0]['totalSum']
    criteria = [doc for doc in mongo.db.criteria.find({})]
    for criterion in criteria:
        mongo.db.criteria.update_one({"name": criterion['name']}, {
            '$set': {
                'percentage': float("{:.2f}".format(criterion['weight'] / total_sum * 100))
            }
        })

    return 'Ok', 200


@app.route("/providers/criteria/<criterion_name>", methods=['PUT'])
@jwt_required
def update_criterion(criterion_name):
    new_data = json_util.loads(request.data)
    behavior = new_data['behavior']
    percentage = 0
    weight = new_data['weight']
    mongo.db.criteria.update_one({"name": criterion_name}, {
        '$set': {
            "behavior": behavior,
            "weight": weight,
            "percentage": percentage
        }
    })
    percentage_update()
    return 'Ok', 200


@app.route("/providers/criteria/<criterion_name>", methods=['GET'])
@jwt_required
def get_criterion(criterion_name):
    criterion = mongo.db.criteria.find_one({"name": criterion_name})
    return json_util.dumps({'criterion': criterion}), 200


@app.route('/providers/criteria/<criterion_name>', methods=['DELETE'])
@jwt_required
def delete_criterion(criterion_name):
    mongo.db.criteria.delete_one({"name": criterion_name})
    percentage_update()
    return 'ok', 200


""" END CLOUD PROVIDER CRITERIA BEHAVIOR """


@app.route('/providers', methods=['POST'])
@jwt_required
def set_provider():
    new_provider = json_util.loads(request.data)
    mongo.db.providers.insert_one(new_provider)
    return 'ok', 200


@app.route('/providers', methods=['GET'])
@jwt_required
def get_providers():
    providers = [doc for doc in mongo.db.providers.find({})]
    return json_util.dumps({'providers': providers}), 200


@app.route('/providers/<provider_name>', methods=['GET'])
@jwt_required
def get_provider(provider_name):
    provider = mongo.db.providers.find_one({'name': provider_name})
    return json_util.dumps({'provider': provider}), 200


@app.route('/providers/<provider_name>', methods=['PUT'])
@jwt_required
def update_provider(provider_name):
    reliability = request.json['reliability']
    flexibility = request.json['flexibility']
    maturity = request.json['maturity']
    datasecurity = request.json['datasecurity']
    geodispatching = request.json['geodispatching']
    price = request.json['price']
    mongo.db.providers.update_one({'name': provider_name}, {'$set': {"reliability": reliability,
                                                                     "flexibility": flexibility,
                                                                     "maturity": maturity,
                                                                     "datasecurity": datasecurity,
                                                                     "geodispatching": geodispatching,
                                                                     "price": price
                                                                     }
                                                            })
    return 'ok', 200


@app.route('/providers/<provider_name>', methods=['DELETE'])
@jwt_required
def delete_provider(provider_name):
    mongo.db.providers.delete_one({'name': provider_name})
    return provider_name + ' deleted with success', 200


""" END CRUD PROVIDERS BEHAVIORS """

""" CLOUD PROVIDERS PRICING """


@app.route('/providers/pricing', methods=['GET'])
@jwt_required
def get_all_pricing():
    pricings = [doc for doc in mongo.db.pricing.find({})]
    return json_util.dumps({'pricings': pricings}), 200


@app.route('/providers/pricing', methods=['POST'])
@jwt_required
def set_pricing():
    new_pricing = json_util.loads(request.data)
    mongo.db.pricing.insert_one(new_pricing)
    return 'ok', 200


@app.route('/providers/pricing/<provider>/<category>', methods=['GET'])
@jwt_required
def detail_pricing(provider, category):
    pricing = mongo.db.pricing.find_one({'provider': provider, 'category': category})
    return json_util.dumps({'pricing': pricing}), 200


@app.route('/providers/pricing/<provider>/<category>', methods=['DELETE'])
@jwt_required
def delete_pricing(provider, category):
    mongo.db.pricing.delete_one({"provider": provider, "category": category})
    return 'ok', 200


@app.route("/providers/pricing/<provider>/<category>", methods=['PUT'])
@jwt_required
def update_pricing(provider, category):
    cpu = request.json['cpu']
    ram = request.json['ram']
    price_per_hour = request.json['pricePerHour']
    price_per_month = request.json['pricePerMonth']
    mongo.db.pricing.update_one({'provider': provider, 'category': category}, {
        '$set': {
            'cpu': cpu, 'ram': ram, 'pricePerHour': price_per_hour, 'pricePermonth': price_per_month
        }
    })
    return 'ok', 200


""" END CLOUD PROVIDERS PRICING """

""" USER MANAGEMENT SECTION"""


@app.route('/users', methods=['GET'])
def get_users():
    user_data = [doc for doc in mongo.db.users.find({})]
    return json_util.dumps({"users": user_data}), 200


@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    mongo.db.users.delete_one({"username": username})
    return {
               'message': 'user remove successfully'
           }, 200

""""
@app.before_first_request
def setup_admin():
    hashed_password = Bcrypt.generate_password_hash(Bcrypt, 'first_password')
    try:
        mongo.db.users.insert_one({"username": 'admin', "email": "fmoussa@ept.sn", "password": hashed_password,
                                   "role": "admin"})
        text = "count are successfully created"
    except:
        text = "count already exist !!"
    msg = Message()
    msg.subject = "Mail de recuperation de password "
    msg.recipients = ["fmoussa@ept.sn"]
    msg.sender = 'kallahbenakhmeth@gmail.com'
    msg.body = 'Admin Count Credential'
    msg.html = render_template_string('<h4>You are the admin of our plateforme please connect with this credentiel</h4>\
           <h4>username: <strong>admin</strong></h4> <h4> password: <strong>first_password</strong></h4> <h4> status:\
                                      {{text}}</h4>', text=text)
    mail.send(msg)
    print("doing something important with %s")
"""

""" END USER MANAGEMENT SECTION """

""" RULES FIELDS"""


@app.route('/fields/<namespace>', methods=['GET'])
def get_fields(namespace):
    try:
        fields_data = [doc for doc in mongo.db.fields[namespace].find({})]
        return json_util.dumps({"conditions": fields_data, "namespace": namespace}), 200
    except:
        return {'message': 'error occur  during process !!'}, 500


@app.route('/fields/<namespace>', methods=['POST'])
def set_field(namespace):
    try:
        new_field = json_util.loads(request.data)
        mongo.db.fields[namespace].insert_one(new_field)
        return {'message': 'field added !'}, 200
    except:
        return {'error': 'error occur  during process !!'}, 500


@app.route('/fields/<namespace>/<criterion>', methods=['DELETE'])
def delete_attribute(namespace, criterion):
    try:
        mongo.db.fields[namespace].detele_one({"criterion": criterion})
        return { 'message': 'criterion deleted successfully !!!'}, 200
    except:
        return { 'error': 'error occur during process !!!'}, 500



@app.route('/fields/<namespace>/<criterion>', methods=['UPDATE'])
def update_attribute(namespace, criterion):
    try:
        criterion = request.json['criterion']
        conditions = request.json['conditions']
        mongo.db.fields[namespace].update_one({'criterion': criterion},{
        '$set': {
            'conditions': conditions
        }
        })
        return {'message': 'ok'}, 200

    except:
        return {'error': 'failed !'}, 500

        
""" END RULES FIELDS"""
if __name__ == '__main__':
    app.run()
