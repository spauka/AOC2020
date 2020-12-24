inp = "942387615"
#inp = "389125467"

class LinkedListNode:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

    def __repr__(self):
        return f"LinkedListNode({self.prev.val} <- {self.val} -> {self.next.val})"

class CircularLinkedList:
    def __init__(self, inp=None):
        self.first = None
        self.last = None
        self.curr = None
        self.max = None
        self.nodes = {}
        if inp is not None:
            for i in inp:
                self.append(int(i))

    def __repr__(self):
        items = []
        curr = self.first
        while True:
            if curr is self.curr:
                items.append(f"({curr.val})")
            else:
                items.append(f"{curr.val}")
            curr = curr.next
            if curr is self.first:
                break
        return f"CircularLinkedList({', '.join(items)})"

    def append(self, val):
        new_node = LinkedListNode(val, self.last, self.first)
        if self.first is None:
            self.first = self.last = self.curr = new_node
            new_node.prev = new_node
            new_node.next = new_node
            self.max = val
        else:
            self.first.prev = new_node
            self.last.next = new_node
            self.last = new_node
            self.max = max(self.max, val)
        self.nodes[val] = new_node

    def insert_after(self, node, val):
        new_node = LinkedListNode(val, node, node.next)
        new_node.next.prev = new_node
        node.next = new_node

    def insert_cll_after(self, node, cll):
        cll.first.prev = node
        cll.last.next = node.next

        node.next.prev = cll.last
        node.next = cll.first

    def remove(self, node):
        if node.prev is node:
            # One element in list
            self.first = None
            self.last = None
            self.curr = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.next = node.prev = None
        return node

    def remove_range(self, node, n):
        first = last = node
        if first is self.first:
            self.first = first.prev
        if first is last:
            self.last = last.next
        for i in range(n-1):
            last = last.next
            if last is self.first:
                self.first = first.prev
            if last is self.last:
                self.last = last.next
            if last is first:
                raise ValueError("List wrapped around!")
        first.prev.next = last.next
        last.next.prev = first.prev

        first.prev = last
        last.next = first

        # Return new linked list
        nll = CircularLinkedList()
        nll.first = first
        nll.last = last
        nll.curr = first
        return nll

    def find(self, val):
        return self.nodes[val]

    def list_vals(self, from_node=None):
        items = []
        if from_node is None:
            curr = self.first
        else:
            curr = from_node
        while True:
            if curr is self.curr:
                items.append(curr.val)
            else:
                items.append(curr.val)
            curr = curr.next
            if curr is self.first:
                break
        return items


c = CircularLinkedList(inp)
#print(c)

for i in range(100):
    curr = c.curr
    pickup = c.remove_range(curr.next, 3)
    vals = pickup.list_vals()
    nval = curr.val - 1
    while nval in vals or nval == 0:
        nval = nval - 1
        if nval <= 0:
            nval = c.max
    nextn = c.find(nval)
    c.insert_cll_after(nextn, pickup)
    c.curr = curr.next

first = c.find(1)
cnode = first.next
vals = []
while cnode is not first:
    vals.append(str(cnode.val))
    cnode = cnode.next
print(f"Part 1: {''.join(vals)}")

c = CircularLinkedList(inp)
print(c)
for v in range(c.max+1, 1_000_000+1):
    if v%1000 == 0:
        print(f"v: {v:010}", end="\r")
    c.append(v)

for i in range(10_000_000):
    if i % 10_000 == 0:
        print(f"i: {i:010}", end="\r")
    curr = c.curr
    pickup = c.remove_range(curr.next, 3)
    vals = pickup.list_vals()
    nval = curr.val - 1
    while nval in vals or nval == 0:
        nval = nval - 1
        if nval <= 0:
            nval = c.max
    nextn = c.find(nval)
    c.insert_cll_after(nextn, pickup)
    c.curr = curr.next

first = c.find(1)
part2 = first.next.val * first.next.next.val
print(f"Part 2: {part2}")
