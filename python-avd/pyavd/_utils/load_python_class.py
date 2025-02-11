# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from __future__ import annotations

import importlib

from .._errors import AristaAvdError, AristaAvdMissingVariableError


def load_python_class(module_path: str, class_name: str, parent_class: type | None = None) -> type:
    """
    Load Python Class via importlib


    Parameters
    ----------
    module_path : str
        Path to import the module from
    class_name : str
        Name of the class to load
    parent_class : type
        Class from which the imported class must inherit if present

    Returns
    -------
    type
        The loaded Class (and not an instance of the Class)

    Raises
    ------
    AristaAvdMissingVariableError
        If module_path or class_name are not present

    AristaAvdError
        If importlib fails to load the Class
        If the loaded Class is not inheriting from the optional parent_class
    """
    if not module_path:
        raise AristaAvdMissingVariableError("Cannot load a python class without the module_path set.")
    if not class_name:
        raise AristaAvdMissingVariableError("Cannot load a python class without the class_name set.")

    try:
        cls = getattr(importlib.import_module(module_path), class_name)
    except ImportError as imp_exc:
        raise AristaAvdError(imp_exc) from imp_exc

    if parent_class is not None and not issubclass(cls, parent_class):
        raise AristaAvdError(f"{cls} is not a subclass of {parent_class} class")

    return cls
