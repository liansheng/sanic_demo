#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: wangzebin
@file: data_check.py
@time: 8/5/18 8:08 PM
"""
from functools import wraps
from sanic.exceptions import ServerError, SanicException
import inspect


def typeassert_request(schema):
    print("this is typeassert")

    def decorate(func):
        @wraps(func)
        def wrapper(*args):
            request = args[1]
            data = request.json
            results, error = schema().load(data)
            if error:
                raise SanicException(error)
            return func(*args)

        return wrapper

    return decorate


def typeassert(schema):
    print("this is typeassert")

    def decorate(func):
        # If in optimized mode, disable type checking
        # if not __debug__:
        #     return func

        # # Map function argument names to supplied types
        # sig = signature(func)
        # bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            # schemas = schema
            # if not isinstance(schema, list):
            #     schemas = list(schema)
            # schemas = [tmp() for tmp in schemas]
            results, error = schema().load(kwargs)
            if error:
                raise SanicException(error)
            return func(*args, **results)

        return wrapper

    return decorate


def typeassert_async(schema):
    print("this is typeassert async")

    def decorate(func):
        # If in optimized mode, disable type checking
        # if not __debug__:
        #     return func

        # # Map function argument names to supplied types
        # sig = signature(func)
        # bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        async def wrapper(*args, **kwargs):
            # schemas = schema
            # if not isinstance(schema, list):
            #     schemas = list(schema)
            # schemas = [tmp() for tmp in schemas]
            results, error = schema().load(kwargs)
            if error:
                raise SanicException(error)
            # for tmp_s in schemas:
            #
            # bound_values = sig.bind(*args, **kwargs)
            # # Enforce type assertions across supplied arguments
            # for name, value in bound_values.arguments.items():
            #     if name in bound_types:
            #         if not isinstance(value, bound_types[name]):
            #             raise TypeError(
            #                 'Argument {} must be {}'.format(name, bound_types[name])
            #                 )
            return await func(*args, **results)

        return wrapper

    return decorate


def marshal(data, fields):
    schemas = [field() for field in fields]
    print("ggggggggggggggggg")
    if isinstance(data, (list, tuple)):
        return [marshal(d, fields) for d in data]

    # type = data.get('type')
    for schema in schemas:
        # if type in schema.__class__.__name__.lower():
        result, errors = schema.dump(data)
        print(" begin: ")
        print(schema.__name__())
        print(result, errors)
        if errors:
            for item in errors.items():
                print('{}: {}'.format(*item))
        return result


class MarshalWith(object):
    def __init__(self, fields):
        if not isinstance(fields, list):
            fields = [fields]
        self.fields = fields

    def __call__(self, f):
        @wraps(f)
        async def wrapper(*args, **kwargs):
            resp = await f(*args, **kwargs)
            return marshal(resp, self.fields)

        return wrapper
