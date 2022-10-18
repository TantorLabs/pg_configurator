import sys
import inspect
import traceback
from pkg_resources import parse_version as version
import re


def exception_helper(show_traceback=True):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return "\n".join(
        [
            v for v in traceback.format_exception(exc_type, exc_value, exc_traceback if show_traceback else None)
        ]
    )


def exception_handler(func):
    def f(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            print(exception_helper(show_traceback=True))
    return f


def get_default_args(func):
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
    }


def get_major_version(str_version):
    return version(re.findall(r"(\d+)", str_version)[0])


def print_header(header):
    print("\n\n")
    print("=".join(['=' * 100]))
    print(header)
    print("=".join(['=' * 100]))
