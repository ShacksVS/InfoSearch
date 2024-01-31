import re
import os


PATTERN = r"[^a-zA-Zа-яА-Я'’]"


def normalize_text(text):
    text = re.sub(PATTERN, ' ', text)
    return text


def normalize_file(file_path: str) -> tuple[set[str], int]:
    with open(file_path, "r") as my_file:
        normalized_words = normalize_text(my_file.read()).split()
        words = len(normalized_words)

        return set(normalized_words), words


def write_result(collection: str):
    with open("results.txt", "w") as output_file:
        output_file.write(collection)


def read_file(file_name: str):
    with open(file_name, "r") as file:
        print(file.read())


if __name__ == "__main__":
    collection = set()
    total_kb = 0
    total_words = 0

    for i in range(1, 11):
        file_name = f"../resources/text{i}.txt"
        unique_words, words_in_file = normalize_file(file_name)

        collection.update(unique_words)
        total_words += words_in_file
        total_kb += os.path.getsize(file_name)

    write_result(str(collection))

    print(f"Total kb in files: {total_kb / 1000}")
    print(f"Total words in files: {total_words}")
    print(f"Unique words: {len(collection)}")

    # read_file("results.txt")