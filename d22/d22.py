from typing import List
from collections import deque

class Player:
    def __init__(self, num: int, cards: List):
        self.player_num = num
        self.deck = deque(cards)
        self.initial = tuple(cards)

    @classmethod
    def parse_inp(cls, f):
        pnum = int(f.readline().strip("\n:").split()[-1])
        deck = []
        for line in f:
            if not (line := line.strip()):
                break
            deck.append(int(line))
        return cls(pnum, deck)

    def restore(self):
        self.deck = deque(self.initial)

    @property
    def deckstate(self):
        return tuple(self.deck)
    @property
    def ncards(self):
        return len(self.deck)

    def __repr__(self):
        return f"<Player {self.player_num}. Deck: ({', '.join(str(d) for d in self.deck)})>"

with open("input") as f:
    p1 = Player.parse_inp(f)
    p2 = Player.parse_inp(f)

# Part 1
while p1.ncards and p2.ncards:
    c1, c2 = p1.deck.popleft(), p2.deck.popleft()
    if c1 < c2:
        # Player 2 wins
        p2.deck.append(c2)
        p2.deck.append(c1)
    else:
        p1.deck.append(c1)
        p1.deck.append(c2)

winner = p1 if p1.ncards else p2
part1 = 0
ncards = winner.ncards
for i, c in enumerate(winner.deck):
    part1 += c * (ncards-i)
print(f"Part 1: {part1}")

# Part 2
def recursive_combat(p1, p2, level=0):
    seen_stacks = set()
    while p1.ncards and p2.ncards:
        # Check if we've seen this state before
        deckstate = (p1.deckstate, p2.deckstate)
        if deckstate in seen_stacks:
            return p1
        seen_stacks.add(deckstate)

        c1, c2 = p1.deck.popleft(), p2.deck.popleft()
        if c1 > p1.ncards or c2 > p2.ncards:
            # Simple game!
            if c1 < c2: winner = p2
            else: winner = p1
        else:
            # Recurse!
            p1_deck = p1.deck
            p2_deck = p2.deck
            p1.deck = deque(deckstate[0][1:c1+1])
            p2.deck = deque(deckstate[1][1:c2+1])
            winner = recursive_combat(p1, p2, level+1)
            p1.deck = p1_deck
            p2.deck = p2_deck

        # Add the winners cards
        if winner is p1:
            p1.deck.append(c1)
            p1.deck.append(c2)
        else:
            p2.deck.append(c2)
            p2.deck.append(c1)

    # Must have run out of cards. Figure out who won!
    if p1.ncards:
        return p1
    return p2

p1.restore(); p2.restore()
winner = recursive_combat(p1, p2)
part2 = 0
ncards = winner.ncards
for i, c in enumerate(winner.deck):
    part2 += c * (ncards-i)
print(f"Part 2: {part2}")