import numpy as np
from bson.objectid import ObjectId


def newEncoder(o):
    if type(o) == ObjectId:
        return str(o)
    return o.__str__


def compare_vectors():
    vect1 = np.array([67, 4, 81, 5, 2])
    vect2 = np.array([2, 5, 6, 4, 67])
    diffcost = np.dot(vect2, vect1)/(np.linalg.norm(vect2)*np.linalg.norm(vect1))
    return np.abs(diffcost)
