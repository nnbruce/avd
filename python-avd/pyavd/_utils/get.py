# Copyright (c) 2023-2024 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
from .._errors import AristaAvdMissingVariableError


def get(dictionary, key, default=None, required=False, org_key=None, separator="."):
    """
    Get a value from a dictionary or nested dictionaries.

    Key supports dot-notation like "foo.bar" to do deeper lookups.
    Returns the supplied default value or None if the key is not found and required is False.

    Parameters
    ----------
    dictionary : dict
        Dictionary to get key from
    key : str
        Dictionary Key - supporting dot-notation for nested dictionaries
    default : any
        Default value returned if the key is not found
    required : bool
        Fail if the key is not found
    org_key : str
        Internal variable used for raising exception with the full key name even when called recursively
    separator: str
        String to use as the separator parameter in the split function. Useful in cases when the key
        can contain variables with "." inside (e.g. hostnames)

    Returns
    -------
    any
        Value or default value

    Raises
    ------
    AristaAvdMissingVariableError
        If the key is not found and required == True
    """

    if org_key is None:
        org_key = key
    keys = str(key).split(separator)
    value = dictionary.get(keys[0])
    if value is None:
        if required is True:
            raise AristaAvdMissingVariableError(org_key)
        return default

    if len(keys) > 1:
        return get(value, separator.join(keys[1:]), default=default, required=required, org_key=org_key, separator=separator)

    return value


def get_v2(dict_or_object, key_or_attribute, default=None, required=False, org_key=None, separator="."):
    """
    Get a value from a dictionary or object or nested dictionaries and objects.

    Key supports dot-notation like "foo.bar" to do deeper lookups.
    Returns the supplied default value or None if the key is not found and required is False.

    Parameters
    ----------
    dict_or_object : dict | object
        Dictionary or Object to get key_or_attribute from
    key_or_attribute : str
        Dictionary Key or Object attribute - supporting dot-notation for nested dictionaries and objects
    default : any
        Default value returned if the key is not found
    required : bool
        Fail if the key is not found
    org_key : str
        Internal variable used for raising exception with the full key name even when called recursively
    separator: str
        String to use as the separator parameter in the split function. Useful in cases when the key
        can contain variables with "." inside (e.g. hostnames)

    Returns
    -------
    any
        Value or default value

    Raises
    ------
    AristaAvdMissingVariableError
        If the key is not found and required == True
    """

    if org_key is None:
        org_key = key_or_attribute
    keys = str(key_or_attribute).split(separator)
    if callable(getattr(dict_or_object, "get", None)):
        value = dict_or_object.get(keys[0])
    else:
        value = getattr(dict_or_object, keys[0], None)

    if value is None:
        if required is True:
            raise AristaAvdMissingVariableError(org_key)
        return default

    if len(keys) > 1:
        return get_v2(value, separator.join(keys[1:]), default=default, required=required, org_key=org_key, separator=separator)

    return value
