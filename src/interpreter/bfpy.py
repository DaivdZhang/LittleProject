class Tape(object):
    def __init__(self):
        self.tape = [0]
        self.index = 0

    def move(self, direction):
        self.index += 1*direction
        if self.index == len(self.tape):
            self.tape.append(0)
        elif self.index < 0:
            self.index = 0
            self.tape.insert(0, 0)

    def inc(self):
        self.tape[self.index] += 1

    def dec(self):
        self.tape[self.index] -= 1

    def set(self, value):
        self.tape[self.index] = value

    def get(self):
        return self.tape[self.index]


def parse(text):
    token_set = {'>', '<', '+', '-', ',', '.', '[', ']'}
    return [x for x in text if x in token_set]


def evaluate(ast):
    tape = Tape()
    p = 0
    psw = 0
    ast_length = len(ast)

    while psw < ast_length:
        token = ast[psw]
        if token == '>':
            tape.move(1)
        elif token == '<':
            tape.move(-1)
        elif token == '+':
            tape.inc()
        elif token == '-':
            tape.dec()
        elif token == ',':
            tape.set(ord(input()))
        elif token == '.':
            print(chr(tape.get()), end='')
        elif token == '[':
            p = psw
            if not tape.tape[tape.index]:
                while ast[psw] != ']':
                    psw += 1
        elif token == ']':
            if tape.tape[tape.index]:
                psw = p + 1
                continue
        psw += 1
