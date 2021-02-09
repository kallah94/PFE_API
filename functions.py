import numpy as np


def setup(data):
    global application_type
    global len_dep
    global len_connected_app
    global number_of_vm
    global sla
    global environment
    global data_size
    global cost_estimation

    try:
        application_type = data["applicationType"]
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
    return {"complexity": complexity_rate(), "availability": availability_rate(), "criticity": criticity_rate()}


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
    if str.lower(application_type) == 'micro':
        rate += 5
    else:
        rate += 12
    if len_dep == 0:
        pass
    elif len_dep <= 5:
        rate += 3
    elif len_dep <= 10:
        rate += 8
    else:
        rate += 5
    if len_connected_app == 0:
        pass
    elif len_connected_app <= 4:
        rate += 3
    elif len_connected_app <= 10:
        rate += 9
    else:
        rate += 15
    if number_of_vm <= 3:
        rate += 1
    elif number_of_vm <= 7:
        rate += 3
    else:
        rate += 5
    return rate


def availability_rate():
    avaibability_rate = 0
    if sla == 2:
        avaibability_rate += 20
    if sla == 4:
        avaibability_rate += 15
    if sla == 8:
        avaibability_rate += 10
    if sla == 12:
        avaibability_rate += 5
    return avaibability_rate


def criticity_rate():
    rate = 0
    if str.lower(environment) == 'dev':
        rate += 2
    if str.lower(environment) == 'test':
        rate += 3
    if str.lower(environment) == 'prod':
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


def compare_vectors(vector_rule, vector_project):
    vect1 = np.array(vector_rule)
    vect2 = np.array(vector_project)
    diff_cost = np.dot(vect2, vect1) / (np.linalg.norm(vect2) * np.linalg.norm(vect1))
    result = np.abs(diff_cost)
    return result
