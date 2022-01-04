from sqlalchemy import inspect

"""
    This function will convert database query object to dictionary
    params : single row of database object
    returns : dictionary format
"""
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


def return_res(msg, code):
    return {
        "code": code.value,
        "result": msg
    }, code.value


def return_error_res(res, error_msg, code):
    res.set_error_msg(error_msg)
    res.set_code(code)
    return res.response, code.value
