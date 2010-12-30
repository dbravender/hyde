"""
Generic loader of extensions (plugins & templates)
"""
import sys

from hyde.exceptions import HydeException

plugins = {}
templates = {}


def load_python_object(name):
    """
    Loads a python module from string
    """
    (module_name, _, object_name) = name.rpartition(".")
    if module_name == '':
        (module_name, object_name) = (object_name, module_name)
    try:
        module = __import__(module_name)
    except ImportError:
        raise HydeException("The given module name [%s] is invalid." %
                            module_name)

    if object_name == '':
        return module

    try:
        module = sys.modules[module_name]
    except KeyError:
        raise HydeException("Error occured when loading module [%s]" %
                            module_name)

    try:
        return getattr(module, object_name)
    except AttributeError:
        raise HydeException("Cannot load the specified plugin [%s]. "
                            "The given module [%s] does not contain the "
                            "desired object [%s]. Please fix the"
                            "configuration or ensure that the module is "
                            "installed properly" %
                            (name, module_name, object_name))