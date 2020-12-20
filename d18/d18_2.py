import tokenize

lines = []
with open("input_s") as f:
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
        if self.op.exact_type == tokenize.PLUS:
            return self.left.value() + self.right.value()
        elif self.op.exact_type == tokenize.STAR:
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

def parse_const(inp, loc):
    """
    Parse bottom level identifiers. These are constants or parenthesized expressions
    """
    csym = inp[loc]
    if csym.exact_type == tokenize.LPAR:
        expr, end = parse_multiplications(inp, loc+1)
        if inp[end].exact_type != tokenize.RPAR:
            raise RuntimeError(f"Expecting token: ). Got {inp[end]}.")
        return Paren(expr), end+1
    elif csym.type == tokenize.NUMBER:
        return Number(csym), loc+1
    else: raise RuntimeError(f"Invalid token: {csym}")

def parse_additions(inp, loc):
    """
    Parse additions
    """
    start_node, loc = parse_const(inp, loc)
    cnode = inp[loc]
    while cnode.exact_type == tokenize.PLUS:
        end_node, loc = parse_const(inp, loc+1)
        start_node = Operator(cnode, start_node, end_node)
        cnode = inp[loc]
    return start_node, loc

def parse_multiplications(inp, loc):
    """
    Parse multiplications
    """
    start_node, loc = parse_additions(inp, loc)
    cnode = inp[loc]
    while cnode.exact_type == tokenize.STAR:
        end_node, loc = parse_additions(inp, loc+1)
        start_node = Operator(cnode, start_node, end_node)
        cnode = inp[loc]
    return start_node, loc

def parse(inp):
    if inp[0].type in (tokenize.NEWLINE, tokenize.ENDMARKER):
        return Null(), 0
    return parse_multiplications(inp, 0)

values = 0
for line in lines:
    tree, _ = parse(line)
    print(tree)
    values += tree.value()
print(f"Part 1: {values}")