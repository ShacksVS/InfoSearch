import re
import os


class TextProcessor:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]"):
        self.collection = set()
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.matrix = dict()

    def normalize_text(self, text):
        return re.sub(self.PATTERN, ' ', text).lower()

    def normalize_file(self, file_path: str):
        with open(file_path, "r") as my_file:
            normalized_words = self.normalize_text(my_file.read()).split()
            words = len(normalized_words)
            return set(normalized_words), words

    def process_files(self):
        file_counter = 1
        for file_path in self.file_paths:
            unique_words, words_in_file = self.normalize_file(file_path)

            for word in unique_words:
                if word not in self.matrix:
                    # If the word is not in the matrix, initialize a list of zeros
                    self.matrix[word] = [0] * self.file_number

                # Update the list to indicate the presence of the word in the current file
                self.matrix[word][file_counter - 1] += 1

            self.collection.update(unique_words)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

            print(f"Done with {file_counter}")
            file_counter += 1

    def save_matrix(self, output_file="matrix.txt"):
        with open(output_file, "w") as file:
            for key, value in self.matrix.items():
                file.write(f"{key} -> {value}\n")

    def save_result(self, output_file="results.txt"):
        with open(output_file, "w") as file:
            for word in self.collection:
                file.write(word + '\n')

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Unique words: {len(self.collection)}")
