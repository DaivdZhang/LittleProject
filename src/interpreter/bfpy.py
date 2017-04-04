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


class VMachine(object):
    def __init__(self):
        self.pc = 0
        self.stack = []
        self.mem = Tape()
        self.program = None

    def initialize(self, string):
        self.program = string

    def run(self):
        tokens = parse(self.program)
        tokens_length = len(tokens)

        while self.pc < tokens_length:
            token = tokens[self.pc]

            if token == '>':
                self.mem.move(1)
            elif token == '<':
                self.mem.move(-1)
            elif token == '+':
                self.mem.inc()
            elif token == '-':
                self.mem.dec()
            elif token == ',':
                self.mem.set(ord(input()))
            elif token == '.':
                print(chr(self.mem.get()), end='')
            elif token == '[':
                self.stack.append(self.pc)
                if not self.mem.tape[self.mem.index]:
                    while tokens[self.pc] != ']':
                        self.pc += 1
            elif token == ']':
                if self.mem.tape[self.mem.index]:
                    self.pc = self.stack[-1]
                else:
                    self.stack.pop()
            self.pc += 1


def parse(text):
    token_set = {'>', '<', '+', '-', ',', '.', '[', ']'}
    return [x for x in text if x in token_set]


if __name__ == "__main__":
    vm = VMachine()
    while True:
        try:
            program = input("bfpy> ")
            if program != "exit":
                vm.initialize(program)
                vm.run()
            else:
                break
        except KeyboardInterrupt:
            exit(0)
