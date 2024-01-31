import re


def read_file(file_path: str) -> set:
    with open(file_path, "r") as my_file:
        text = my_file.read()
        text = re.sub(r'[!«"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n]', ' ', text)
        words = text.split()
        return set(words)


if __name__ == "__main__":
    result = set()
    for i in range(1, 11):
        file_name = f"../resources/text{i}.txt"
        result.update(read_file(file_name))

    print(result)
    print(f"Unique words: {len(result)}")
