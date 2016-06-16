import os
import sys
import linecache


def trace(func):
    """
    A trace decorator
    from: https://zhuanlan.zhihu.com/p/20175869

    :param func:
    :return:
    """
    def globaltrace(frame, why, arg):
        if why == "call":
            return localtrace
        return None

    def localtrace(frame, why, arg):
        if why == "line":
            filename = frame.f_code.co_filename
            line_no = frame.f_lineno
            b_name = os.path.basename(filename)
            tmp = linecache.getline(filename, line_no)
            print("{0}({1}):{2}".format(b_name, line_no, tmp), end='')
        return localtrace

    def _func(*args, **kwargs):
        sys.settrace(globaltrace)
        result = func(*args, **kwargs)
        sys.settrace(None)
        return result
    return _func


@trace
def foo(i):
    string = "Hello world!"
    print(string)
    print(string[i])
    os.system("cls")


if __name__ == "__main__":
    foo(-1)
