import re

def print_error(data: str, index: int, length: int, message: str):
    print(data)
    print(' ' * index + '^' * length)
    print(message)

def tokenize(data: str):
    index = 0
    while index < len(data):
        if data[index] in ' \t\n':
            index += 1
            continue
        m = re.match('^(([0-9]+(\\.[0-9]+)?)|[-+*/^()])', data[index:])
        if m:
            span = m.span()
            yield (index, span[1], data[index:index+span[1]])
            index += span[1]
        else:
            print_error(data, index, 1, 'invalid token')
            exit(1)

class TokenReader:
    def __init__(self, data: str):
        self.data = data
        self.tokens = list(tokenize(data))
        self.i = 0

    @property
    def current(self):
        if self.i >= len(self.tokens):
            return None
        if self.tokens[self.i][2][0] in '0123456789':
            return float(self.tokens[self.i][2])
        return self.tokens[self.i][2]

    def expect(self, expected: str):
        if self.i >= len(self.tokens):
            print_error(self.data, len(self.data), 1, f'expected: {expected}')
            exit(1)
        print_error(self.data, self.tokens[self.i][0], len(self.tokens[self.i][1]), f'expected: {expected}')

    def next(self):
        self.i += 1

def add_sub(reader: TokenReader) -> float:
    first = div_mul(reader)
    while reader.current in ['+', '-']:
        if reader.current == '+':
            reader.next()
            first += div_mul(reader)
        if reader.current == '-':
            reader.next()
            first -= div_mul(reader)
    return first

def div_mul(reader: TokenReader) -> float:
    first = power(reader)
    while reader.current in ['*', '/']:
        if reader.current == '*':
            reader.next()
            first *= power(reader)
        if reader.current == '/':
            reader.next()
            first /= power(reader)
    return first

def power(reader: TokenReader) -> float:
    first = unary(reader)
    while reader.current == '^':
        reader.next()
        first = first ** unary(reader)
    return first

def unary(reader: TokenReader) -> float:
    sign = 1
    while reader.current in ['+', '-']:
        if reader.current == '-':
            sign *= -1
        reader.next()
    return item(reader) * sign

def item(reader: TokenReader) -> float:
    if reader.current == '(':
        reader.next()
        result = add_sub(reader)
        if reader.current != ')':
            reader.expect(')')
        reader.next()
        return result
    if isinstance(reader.current, float):
        value = reader.current
        reader.next()
        return value
    reader.expect('number')

print(add_sub(TokenReader(input('>>> '))))
