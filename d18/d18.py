import tokenize

lines = []
with open("input") as f:
    line = []
    for token in tokenize.generate_tokens(f.readline):
        line.append(token)
        if token.type in (tokenize.NEWLINE, tokenize.ENDMARKER):
            lines.append(line)
            line = []
    if line:
        lines.append(line)

class Node:
    def value(self):
        raise NotImplementedError("Not Implemented")

class Operator(Node):
    def __init__(self, op: tokenize.TokenInfo, left: Node, right: Node):
        self.op = op
        self.left = left
        self.right = right
    def value(self):
        if self.op.string == "+":
            return self.left.value() + self.right.value()
        elif self.op.string == "*":
            return self.left.value() * self.right.value()
        raise NotImplementedError("Unknown Operator")
    def __repr__(self):
        return f"{self.op.string} ({self.left}) ({self.right})"

class Null(Node):
    def value(self):
        return 0
    def __repr__(self):
        return ""

class Number(Node):
    def __init__(self, value: tokenize.TokenInfo):
        self._value = value
    def value(self):
        return int(self._value.string)
    def __repr__(self):
        return self._value.string

class Paren(Node):
    def __init__(self, root: Node):
        self.root = root
    def value(self):
        return self.root.value()
    def __repr__(self):
        return f"({self.root})"

def parse_token(inp, loc):
    csym = inp[loc]
    if csym.exact_type == tokenize.LPAR:
        expr, end = parse_expr(inp, loc+1)
        if inp[end].exact_type != tokenize.RPAR:
            raise RuntimeError(f"Expecting token: ). Got {inp[end]}.")
        return Paren(expr), end+1
    elif csym.type == tokenize.NUMBER:
        return Number(csym), loc+1
    else: raise RuntimeError("Invalid token: {csym}")

def parse_expr(inp, loc):
    if inp[loc].type in (tokenize.NEWLINE, tokenize.ENDMARKER):
        raise RuntimeError(f"Unexpected end of expression. Got {inp[loc]}.")
    start_node, loc = parse_token(inp, loc)
    while True:
        nsym = inp[loc]
        if nsym.exact_type in (tokenize.NEWLINE, tokenize.ENDMARKER, tokenize.RPAR):
            return start_node, loc
        elif nsym.exact_type in (tokenize.PLUS, tokenize.STAR):
            end_node, loc = parse_token(inp, loc+1)
            start_node = Operator(nsym, start_node, end_node)
        else:
            raise RuntimeError(f"Unexpected token: {nsym}. Expecting an operator or end of expression.")

def parse(inp):
    if inp[0].type in (tokenize.NEWLINE, tokenize.ENDMARKER):
        return Null(), 0
    return parse_expr(inp, 0)

values = 0
for line in lines:
    tree, _ = parse(line)
    values += tree.value()
print(f"Part 1: {values}")