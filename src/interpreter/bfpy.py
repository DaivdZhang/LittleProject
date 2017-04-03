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
    pc = 0
    ast_length = len(ast)

    while pc < ast_length:
        token = ast[pc]
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
            p = pc
            if not tape.tape[tape.index]:
                while ast[pc] != ']':
                    pc += 1
        elif token == ']':
            if tape.tape[tape.index]:
                pc = p + 1
                continue
        pc += 1

if __name__ == "__main__":
    while True:
        program = input("bfpy> ")
        try:
            if program != "exit":
                evaluate(parse(program))
            else:
                break
        except KeyboardInterrupt:
            exit(0)
