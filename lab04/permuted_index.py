import re
import os
import time


class PermutedIndex:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]",stop_words=None):
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.permuted_index_size = 0
        self.permuted_dict = dict()
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

            self.fill_permuted_index(cleaned_words)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

            print(f"Done with {file_counter}")
            file_counter += 1

        self.save_dict()
        # self.print_summary()

    def count_words_in_file(self, cleaned_file: list) -> int:
            return len(cleaned_file)

    # toDo
    def fill_permuted_index(self, words):
        for word in words:
            if word not in self.permuted_dict:
                permuted_word = word_transformation(word)
                self.permuted_dict[word] = permuted_word

            # permuted_word = word_transformation(word)
            # for element in permuted_word:
            #     if element not in self.permuted_dict:
            #         self.permuted_dict[element] = []
            #
            #     if counter not in self.permuted_dict[element]:
            #         self.permuted_dict[element].append(counter)

    def save_dict(self, output_file="../lab04/texts/permuted-index.txt"):
        with open(output_file, "w") as file:
            for key, value in self.permuted_dict.items():
                value = " -> ".join(map(str, value))
                file.write(f"{key}\t {value}\n")
        self.permuted_index_size = os.path.getsize(output_file)

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Two words index size: {self.permuted_index_size / 1000} KB")

    # t*ras - > ras$t
    # *aras -> aras$
    # tara* -> $tara
    def search(self, word: str):
        to_find = str()

        if "*" in word:
            parts = word.split("*")
            if len(parts) == 2:
                before, after = parts
                to_find = after + "$" + before
            elif word.startswith("*"):
                to_find = word[1:] + "$"
            elif word.endswith("*"):
                to_find = "$" + word[:-1]

            found = [key for key, value in self.permuted_dict.items() if any(to_find in element for element in value)]

            print(found)
        else:
            print("Invalid search format. Please include '*' in your search term.")


def word_transformation(word):
    transformations = []
    for i in range(len(word) + 1):
        transformed_word = word[i:] + '$' + word[:i]
        transformations.append(transformed_word)
    return transformations