import re

from three_gram_index import ThreeGramIndex
from permuted_index import PermutedIndex
from Tree import BinaryTree



def normalize_text(text):
    pattern = r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]"
    return re.sub(pattern, ' ', text).lower()


def clean_file(file_path: str):
    words = list()
    with open(file_path, "r") as my_file:
        words.extend(normalize_text(my_file.read()).split())

    return words


if __name__ == "__main__":
    stop_words = ["і", "на", "у", "в", "а", "з", "зі", "до"]

    words = list()
    for i in range(1, 11):
        words.extend(clean_file(f"../resources/text{i}.txt"))

    bt = BinaryTree(words)
    print(bt.search("тар*"))
    print(bt.search("ш*ко"))
    print(bt.search("*енко"))

    # permuted_index = PermutedIndex(stop_words=stop_words)
    # permuted_index.process_files()
    # permuted_index.search("тара*")
    # permuted_index.search("т*ас")
    # permuted_index.search("*ченко")

    three_gram = ThreeGramIndex(stop_words=stop_words)
    three_gram.process_files()
    three_gram.search("шев*нко")
    three_gram.search("ди*тія")
    # three_gram.search("шевч*")
