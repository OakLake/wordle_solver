import re
import string
from typing import List, Tuple

from nltk.corpus import words


ALPHABET = string.ascii_lowercase


def get_wordbase(num_letters) -> List[str]:
    import nltk

    nltk.download("words")

    word_base = [word for word in words.words() if len(word) == num_letters]

    return word_base


def constrain_regex(
    knows_at_letters: str, known_not_at_letters: List[str], restricted_letters: List[str]
) -> str:
    alphabet = [alpha for alpha in ALPHABET if alpha not in restricted_letters]

    letter_options = []
    for known_at, known_not_at in zip(knows_at_letters, known_not_at_letters):
        if len(known_at) != 0:
            letter_options.append(known_at)
        else:
            letter = "".join([l for l in alphabet if l not in known_not_at])
            letter_options.append(letter)

    rgx = ("^" + "[{}]{{1}}" * len(letter_options) + "$").format(*letter_options)

    return rgx


def display(items: List[str], chunk_size: int = 25) -> None:
    print("\nChoose one from:\n")
    for chunk_ix in range(0, len(items), chunk_size):
        print(*items[chunk_ix : chunk_ix + chunk_size], sep=" | ")


def get_player_input(
    known_at_letters, known_not_at_letters, restricted_letters
) -> Tuple[List[str], List[str], List[str]]:
    kal_input = input(f"Known at letters, e.g *it**. Current ='{known_at_letters}' : ")
    knal_input = (
        input(
            f"Known not at letters, e.g ****r. Current = '{known_not_at_letters}' : "
        )
    )
    rl_input = input(f"New restricted letters (current= '{restricted_letters}'): ")

    kal = [l if l != "*" else "" for l in list(kal_input or known_at_letters)]
    knal = list(known_not_at_letters)
    for ix, l in enumerate(list(knal_input or "")):
        if l != "*":
            knal[ix].append(l)
    rl = list(rl_input or "") + restricted_letters

    return kal, knal, rl


def play(num_letters=5):

    wordbase = get_wordbase(num_letters)

    # Initial values
    known_at_letters = ["" for _ in range(num_letters)]
    known_not_at__letters = [[] for _ in range(num_letters)]
    restricted_letters = []

    for iter_ix in range(1, 7):
        print(f"\n\nIteration {iter_ix} ~~~~~~~~~~ {known_at_letters}\n")
        known_at_letters, known_not_at__letters, restricted_letters = get_player_input(
            known_at_letters, known_not_at__letters, restricted_letters
        )

        rgx = constrain_regex(
            known_at_letters, known_not_at__letters, restricted_letters
        )

        solvers = [word for word in wordbase if re.search(rgx, word)]
        display(solvers)


if __name__ == "__main__":
    play()
