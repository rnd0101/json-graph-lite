def obj_to_dict(obj, attrs, d=None):
    d = d or {}
    for attr in attrs:
        value = getattr(obj, attr, None)
        if value is not None:
            d[attr] = value
    return d


def check_type(value, type):
    if isinstance(value, type):
        return value
    raise TypeError("Type {} expected".format(type.__name__))


def check_condition(value, condition, error_message):
    if condition(value):
        return value
    raise ValueError(error_message)


def only_keys(d, keys):
    return {k: v for (k, v) in d.iteritems() if k in keys}


def inplace_update(d, **other):
    d.update(other)
    return d


def inplace_del(d, key):
    del d[key]
    return d


def search_by_criteria(objects, criteria):
    if callable(criteria):
        return [node for node in objects if criteria(node)]
    raise ValueError("Criteria is not callable.")
