"""Persistance for python objects

.. Authors:
    Philippe Dessauw
    philippe.dessauw@nist.gov

.. Sponsor:
    Alden Dima
    alden.dima@nist.gov
    Information Systems Group
    Software and Systems Division
    Information Technology Laboratory
    National Institute of Standards and Technology
    http://www.nist.gov/itl/ssd/is
"""
import cPickle
import pickle


def save(obj, filename):
    """Dump an object to a given file

    Parameters:
        obj: The python object that you want to store
        filename (:func:`str`): Name of the file to store the object
    """
    with open(filename, "wb") as pickle_file:
        cPickle.dump(obj, pickle_file, pickle.HIGHEST_PROTOCOL)


def load(filename):
    """Load an object from a filename

    Parameters:
        filename (:func:`str`): Name of the file storing the object

    Returns:
        obj: Object contained inside the file
    """
    with open(filename, "rb") as pickle_file:
        obj = cPickle.load(pickle_file)

    return obj
