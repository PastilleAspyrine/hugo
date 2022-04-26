
import random
from lully import window
from itertools import islice
from collections import defaultdict, deque


with open('../../merdier/claude-gueux.txt') as fd:
    text = fd.read().lower()

def text_to_words(text: str) -> set[str]:
    text = text.replace('\n', ' ').replace("œ", 'oe').replace("-", ' ').replace("’", ' ').replace('.', '').replace(',', '').replace(';', '').replace('?', '').replace('!', '')
    return set(m for m in text.split(' ') if len(m) > 1 and not m.isdigit())

words_gueux = text_to_words(text)

with open('../../merdier/dico-fr') as fd:
    words_all = text_to_words(fd.read().lower())


print('MOTS SPÉCIFIQUES À CLAUDE GUEUX:', len(words_gueux - words_all))
print(words_gueux - words_all)
# exit()





def model_from_text(text: str, order: int) -> str:

    occs = defaultdict(lambda: defaultdict(int))
    for *prevs, nxt in window(text, order+1):
        occs[''.join(prevs)][nxt] += 1
    # print('MODEL:', occs)
    nonchoice = sum(1 for choices in occs.values() if len(choices) == 1)
    total = sum(1 for choices in occs.values())
    return occs, nonchoice / total

def generate_from_model(text: str, occs: dict, gensize: int = 100) -> str:
    order = len(next(iter(occs)))

    def le_suivant_de(lettres: str) -> str:
        c = random.choices(tuple(occs[lettres]), weights=occs[lettres].values(), k=1)
        return c[0]

    début = text[:order].lower()

    buffer = deque(début, maxlen=order)


    # print('\n\n\n')
    # print(début, end='')
    out = list(début)
    for _ in range(gensize):
        new = le_suivant_de(''.join(buffer))
        out.append(new)
        buffer.append(new)

    return ''.join(out)



for order in range(5, 6):
    print(f'ORDER: {order}')
    mm, ratio = model_from_text(text, order=order)
    print(f'RATIO LINÉRARITÉ: {round(ratio * 100, 2)}%')
    gen = generate_from_model(text, mm, gensize=10000)
    print(gen)

    def show_set(name: str, words: set) -> print:
        print(f"{name.upper()}:", len(words), tuple(islice(words, 0, 10)))
    words_found = text_to_words(gen)
    show_set('found', words_found)
    show_set('refound', words_found & words_gueux)
    show_set('unpresent', words_found - words_gueux)
    show_set('new', words_found - (words_all | words_gueux))
    print('\n###################\n')
    print(words_found - (words_all | words_gueux))


