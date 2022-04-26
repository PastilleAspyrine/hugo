
import random
from lully import window
from collections import defaultdict


# with open('../../merdier/claude-gueux.txt') as fd:
    # text = fd.read().lower()



text = 'aaaaaaaaabbab'

# print(tuple(window(text)))

occs = defaultdict(lambda: defaultdict(int))
for prev, nxt in window(text):
    occs[prev][nxt] += 1
print(occs)


def le_suivant_de(lettre: str) -> str:
    return random.choices(tuple(occs[lettre]), weights=occs[lettre].values(), k=1)[0]


début = 'a'
début = 'Il y a sept ou huit ans'[0].lower()

for _ in range(100):
    print(début, end='')
    début = le_suivant_de(début)

print()

