import math


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parameters, self.body, self.env = parms, body, env

    def __call__(self, *args, **kwargs):
        return evaluate(self.body, Lisp.Env(self.parameters, args, self.env))


class Environment(dict):
    def __init__(self, parms=(), args=(), outer=None, **kwargs):
        super().__init__(**kwargs)
        self.update(zip(parms, args))
        self.outer = outer

    def search(self, var):
        if var in self:
            return self
        else:
            try:
                return self.outer.search(var)
            except AttributeError:
                print("Error: undefined Symbol '%s'" % var)


class Lisp(object):
    Symbol = str
    Number = (int, float)
    List = list
    Env = Environment
    Proc = Procedure


def std_environment():
    env = Lisp.Env()
    env.update({'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b,
                '/': lambda a, b: a / b, '<': lambda a, b: a < b, '>': lambda a, b: a > b,
                '>=': lambda a, b: a >= b, '<=': lambda a, b: a <= b, "eq?": lambda a, b: a == b,
                "zero?": lambda x: x == 0, "negative?": lambda x: x < 0, "positive?": lambda x: x > 0,
                "odd?": lambda x: x % 2 != 0, "even?": lambda x: x % 2 == 0,
                "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin, "acos": math.acos,
                "atan": math.atan, "sqrt": math.sqrt, "gcd": math.gcd})
    return env


def tokenize(code):
    """

    :type code: str
    :return:
    """
    token = code.replace('(', ' ( ').replace(')', ' ) ').split()
    return token


def read_from_token(token):
    """

    :type token: list
    :return:
    """
    ast = None

    if token[0] == '(':
        ast = []
    sub_ast = ast
    table = {0: sub_ast}
    depth = 0

    while len(token) != 0:
        element = token.pop(0)
        if element == '(':
            sub_ast.append([])
            sub_ast = sub_ast[-1]
            depth += 1
            table.update({depth: sub_ast})
        elif element == ')':
            depth -= 1
            sub_ast = table[depth]
        else:
            sub_ast.append(atom(element))
    return ast[0]


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Lisp.Symbol(token)


def parse(code):
    return read_from_token(tokenize(code))


def evaluate(x, env):
    if isinstance(x, Lisp.Symbol):
        return env.search(x)[x]
    elif not isinstance(x, Lisp.List):
        return x
    elif x[0] == "if":
        _, test, consequent, alt = x
        exp = consequent if evaluate(test, env) else alt
        return evaluate(exp, env)
    elif x[0] == "cond":
        print(x)
        _, *clause = x
        print(clause)
        for i in clause:
            if evaluate(i[0], env):
                return evaluate(i[1], env)
    elif x[0] == "define":
        _, var, exp = x
        env.update({var: evaluate(exp, env)})
    elif x[0] == "quote":
        _, exp = x
        return exp
    elif x[0] == "set!":
        _, var, exp = x
        env.search(var)[var] = evaluate(exp, env)
    elif x[0] == "lambda":
        _, p, body = x
        return Lisp.Proc(p, body, env)
    elif x[0] == "car":
        return evaluate(x[1][0], env)
    elif x[0] == "cdr":
        return [evaluate(i, env) for i in x[1][1:]]
    else:
        proc = evaluate(x[0], env)
        if isinstance(proc, Lisp.Number):
            return proc

        args = [evaluate(arg, env) for arg in x[1:]]
        result = proc(*args)
        return result

if __name__ == "__main__":
    global_env = std_environment()
    while True:
        expression = input("lispy> ")
        if expression == "exit":
            break
        value = evaluate(parse(expression), global_env)
        if value is not None:
            print("> %s" % value)
