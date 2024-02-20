import re
import os
import time


class ThreeGramIndex:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]",stop_words=None):
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.three_gram_size = 0
        self.three_gram_dict = dict()
        self.stop_words = set(stop_words if stop_words else [])

    def normalize_text(self, text):
        return re.sub(self.PATTERN, ' ', text).lower()

    def clean_file(self, file_path: str):
        with open(file_path, "r") as my_file:
            words = self.normalize_text(my_file.read()).split()
            return [word for word in words if word not in self.stop_words]

    def process_files(self):
        file_counter = 1

        for file_path in self.file_paths:

            cleaned_words = self.clean_file(file_path)
            words_in_file = self.count_words_in_file(cleaned_words)

            self.fill_three_gram(cleaned_words)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

            print(f"Done with {file_counter}")
            file_counter += 1

        self.save_dict()
        # self.print_summary()

    def count_words_in_file(self, cleaned_file: list) -> int:
            return len(cleaned_file)

    def fill_three_gram(self, words):
        for word in words:
            three_gram = word_transformation(word)
            for element in three_gram:
                if element not in self.three_gram_dict:
                    self.three_gram_dict[element] = []

                if word not in self.three_gram_dict[element]:
                    self.three_gram_dict[element].append(word)

    def save_dict(self, output_file="../lab04/texts/three-gram-index.txt"):
        with open(output_file, "w") as file:
            for key, value in self.three_gram_dict.items():
                value = " -> ".join(map(str, value))
                file.write(f"{key}\t {value}\n")
        self.three_gram_size = os.path.getsize(output_file)

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Two words index size: {self.three_gram_size / 1000} KB")

    def search(self, word: str):
        prefix, suffix = word.split('*')

        prefix = '$' + prefix
        suffix = suffix + '$'
        prefix_matches = set(self.three_gram_dict.get(prefix[-3:], []))

        suffix_matches = set(self.three_gram_dict.get(suffix[:3], []))

        print(prefix_matches.intersection(suffix_matches))


def word_transformation(word):
    transformations = []
    word = f"${word}$"

    for i in range(len(word) - 2):
        three_gram = word[i:i + 3]
        transformations.append(three_gram)
    return transformations
