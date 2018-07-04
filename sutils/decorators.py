#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""

@version: 0.1
@author:  quantpy
@file:    decorators.py
@time:    2018/4/28 9:25
"""
import sys
import traceback
from functools import wraps, partial
import warnings
from datetime import datetime
import reprlib

from .utils import get_full_parameters


def timeit(func):
    """
    timing decorator
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        time_start = datetime.now()
        print(time_start, func.__name__, 'starts...')
        try:
            ret = func(*args, **kwargs)
        except KeyboardInterrupt:
            print('Interrupted!')
            ret = None
        time_end = datetime.now()
        print(time_end, func.__name__, 'finished.')
        print('Total time used: {!s}'.format(time_end - time_start), '\n')

        return ret

    return wrapper


def timer(level=1, file=sys.stdout):
    def decorate(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            printf = partial(print, file=file)
            time_start = datetime.now()
            if level >= 1:
                printf(time_start, func.__name__, 'starts...')
            if level >= 2:
                args_, kwargs_, _ = get_full_parameters(func, *args, **kwargs)
                parameter_args = reprlib.repr(', '.join(repr(arg) for arg in args_))[1:-1]
                parameter_kwargs = reprlib.repr(', '.join(f'{k}={v!r}' for k, v in kwargs_.items()))[1:-1]
                parameters = ', '.join(filter(bool, [parameter_args, parameter_kwargs]))
                printf(f'Running {func.__name__}({parameters})')
            try:
                ret = func(*args, **kwargs)
            except KeyboardInterrupt:
                print('Interrupted!')
                ret = None

            time_end = datetime.now()
            if level >= 1:
                printf(time_end, func.__name__, 'finished.')
            printf('Total time used: {!s}\n'.format(time_end - time_start))

            return ret
        return decorated_func
    return decorate


def handle_exceptions(*exc_types, handler=None):
    """忽略但警告指定异常"""
    # if not exc_types:
    #     exc_types = (Exception,)

    def wrapper(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except BaseException as e:
                err = traceback.format_exc()
                if isinstance(e, exc_types):
                    if callable(handler):
                        handler(err)
                    else:
                        warnings.warn(repr(err))
                    ret = None
                else:
                    raise e
            return ret
        return wrapped_func
    return wrapper


def filter_warnings(*warning_types, action='ignore'):
    """过滤指定警告类型，如果不指定将过滤所有警告"""
    def wrapper_(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings():
                if warning_types:
                    for warning_type in warning_types:
                        warnings.simplefilter(action, category=warning_type, append=True)
                else:
                    warnings.simplefilter(action, append=True)
                ret = func(*args, **kwargs)
            return ret
        return wrapper
    return wrapper_

