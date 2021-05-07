import operator

import numpy as np
from topsis import topsis

def setup(data):
    global project_architecture
    global len_dep
    global len_connected_app
    global number_of_vm
    global sla
    global environment
    global data_size
    global cost_estimation
    global ram
    global cpu
    global application_type

    try:
        project_architecture = data["projectArchitecture"]
    except KeyError:
        application_type = None

    try:
        len_dep = len(data["dependencies"])
    except KeyError:
        len_dep = None

    try:
        len_connected_app = len(data["connectedApplications"])
    except KeyError:
        len_connected_app = None

    try:
        number_of_vm = data["numberOfVm"]
    except KeyError:
        number_of_vm = None

    try:
        sla = data["SLA"]
    except KeyError:
        sla = None

    try:
        environment = data["environment"]
    except KeyError:
        environment = None
    
    try:
        cost_estimation = data["capex"]
    except KeyError:
        cost_estimation = None

    try:
        cpu = data["cpu"]
    except KeyError:
        cpu = None
    
    try:
        ram = data["memory"]
    except KeyError:
        ram = None
    
    try:
        application_type = data["applicationType"]
    except KeyError:
        application_type = "default"

    return {
        "complexity": complexity_rate(),
        "availability": availability_rate(),
        "criticity": criticity_rate(),
        'application_type': application_type,
        "cpu": cpu,
        "ram": ram
        }


def complexity_rate():
    """
    @applicationType {Sometimes the architecture of our application is important when with wish to deploy or migrate it
    in the cloud. Microservice architecture offer us the possibility to migrate peace by peace and it
    can be simplify the process but. With standalone approach we must migrate the whole application
    at once and it may complicated}
    @dependencies {the number of dependencies can improve the migration or deployment task because with have at least to
    deal with versions of heterogeneous stack of technologies }
    @connectedApplications { when many applications must be connected with our app
    the migration or the deployment in the cloud may be a little bit more complex}
    """
    rate = 0
    if project_architecture == 'micro':
        rate += 5
    else:
        rate += 12
    if len_dep == 0:
        pass
    elif len_dep <= 4:
        rate += 2
    elif len_dep <= 10:
        rate += 8
    else:
        rate += 15
    if len_connected_app == 0:
        pass
    elif len_connected_app <= 4:
        rate += 6
    elif len_connected_app <= 10:
        rate += 15
    else:
        rate += 20
    if number_of_vm <= 3:
        rate += 1
    elif number_of_vm <= 7:
        rate += 3
    elif number_of_vm <= 10:
        rate += 8
    else:
        rate += 15
    return rate


def availability_rate():
    avaibability_rate = 0
    if sla == 2:
        avaibability_rate += 20
    if sla == 4:
        avaibability_rate += 10
    if sla == 8:
        avaibability_rate += 5
    return avaibability_rate


def criticity_rate():
    rate = 0
    if environment == 'dev':
        pass
    if environment == 'test':
        pass
    if environment == 'prod':
        rate += 15
    if len_connected_app == 0:
        pass
    elif len_connected_app <= 4:
        rate += 3
    elif len_connected_app <= 10:
        rate += 9
    else:
        rate += 15
    return rate


def criticity_bound(app_criticity):
    if (app_criticity - criticity_rate()) / criticity_rate() > 0.2:
        return True
    else:
        return False


def price_min_on_premise(categories):
    try:
        min_price = int(cost_estimation)
    except:
        return False
    print(categories)
    for category in categories:
        if int(category["pricePerMonth"]) < min_price:
            min_price = int(category["pricePerMonth"])
    if min_price == cost_estimation:
        return True
    else:
        return False

def compare_vectors(vector_rule, vector_project):
    vect1 = np.array(vector_rule)
    vect2 = np.array(vector_project)
    diff_cost = np.dot(vect2, vect1) / (np.linalg.norm(vect2) * np.linalg.norm(vect1))
    return diff_cost

def app_readyness(vector_rule, vector_project, app_criticity, categories):
    """
    This function decide if the appliation is cloud readyness or not.
    To do that we will compare the lowest possible estimation cost to the public cloud and the onPremise cost estimation
    if onPremise exploitation cost is lower than the LPECPC we will suggest to deployed it in OnPremise
    otherwise we will compare this applications criteria vector with the cloud readyness app criteria vector by the cosinus similarity algorithm.
    If the application is not  at least at 50% compatible we will suggest to deployed in OnPremise.
    """

    if price_min_on_premise(categories):
        return "Deploy On Premise !!!! due to lowest Exploitation Cost"
    if criticity_bound(app_criticity):
        return "Deploy On Premise !!! Application criticy is out of boundaries"
    if compare_vectors(vector_rule, vector_project) >= 0.5 :
        return "deployed in the public cloud"
    else:
        return "deployed On Premise !!! due to an incompatibility with public cloud"

def build_criteria_behavior_matrix(data):
    behavior_matrix = []
    weight_matrix = []
    criteria_names = []
    for doc in data:
        if doc['behavior'] == 'benefit':
            behavior_matrix.append(1)
        else:
            behavior_matrix.append(0)
        criteria_names.append(doc['name'])
        weight_matrix.append(doc['percentage'])
    data = {"behaviors": behavior_matrix, "weights": weight_matrix, "criteria_names": criteria_names}
    print(data)
    return data


def make_provider_list(providers, criteria):
    data = build_criteria_behavior_matrix(criteria)
    criteria_names = data['criteria_names']
    weights = data['weights']
    behaviors = data['behaviors']
    providers_name = []
    providers_criteria_matrix = []
    for provider in providers:
        criteria = []
        providers_name.append(provider['name'])
        for criteria_name in criteria_names:
            try:
                criteria.append(provider[criteria_name])
            except KeyError:
                continue
        providers_criteria_matrix.append(criteria)
    decision = topsis(providers_criteria_matrix, weights, behaviors)
    decision.calc()
    scores = decision.C.tolist()
    result = list(map(lambda item: {'provider': item[0], 'score': item[1]}, zip(providers_name, scores)))
    result.sort(key=operator.itemgetter('score'), reverse=True)
    finalproviders = []
    for provider in result:
        finalproviders.append(provider['provider'])
    return finalproviders
