from sqlalchemy import inspect
"""
    This function will convert database query object to dictionary
    params : single row of database object
    returns : dictionary format
"""
def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}