import numpy as np


def complexity_rate(data):
    rate = 0
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
    try:
        application_type = data["applicationType"]
        if str.lower(application_type) == 'micro':
            rate += 5
        else:
            rate += 12
    except KeyError:
        pass

    try:
        dependencies = data["dependencies"]
        len_dep = len(dependencies)
        if len_dep == 0:
            pass
        elif len_dep <= 5:
            rate += 3
        elif len_dep <= 10:
            rate += 8
        else:
            rate += 5
    except KeyError:
        pass

    try:
        connected_applications = data["connectedApplications"]
        len_connected_app = len(connected_applications)
        if len_connected_app == 0:
            pass
        elif len_connected_app <= 4:
            rate += 3
        elif len_connected_app <= 10:
            rate += 9
        else:
            rate += 15
    except KeyError:
        pass

    try:
        number_of_vm = data["numberOfVm"]
        if number_of_vm <=3:
            rate += 1
        elif number_of_vm <= 7:
            rate += 3
        else:
            rate += 5
    except KeyError:
        pass
    print(rate)
    return rate


def availability_rate(data):
    return None


def criticity_rate(data):
    return None


def compare_vectors():
    vect1 = np.array([67, 4, 81, 5, 2])
    vect2 = np.array([2, 5, 6, 4, 67])
    diffcost = np.dot(vect2, vect1) / (np.linalg.norm(vect2) * np.linalg.norm(vect1))
    return np.abs(diffcost)
