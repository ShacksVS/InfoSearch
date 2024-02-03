import re
import os

import pandas as pd


class TextProcessor:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]"):
        self.collection = set()
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.matrix = dict()
        self.inverted_index = dict()

    def process_files(self):
        file_counter = 1

        for file_path in self.file_paths:

            unique_words = self.clean_file(file_path)
            words_in_file = self.count_words_in_file(unique_words)

            self.fill_matrix(unique_words, file_counter)
            self.fill_inverted_index(unique_words, file_counter)

            self.collection.update(unique_words)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

            print(f"Done with {file_counter}")
            file_counter += 1

        self.save_matrix()
        self.save_inverted_index()
        self.print_summary()

    def normalize_text(self, text):
        return re.sub(self.PATTERN, ' ', text).lower()

    def clean_file(self, file_path: str):
        with open(file_path, "r") as my_file:
            return self.normalize_text(my_file.read()).split()

    def count_words_in_file(self, cleaned_file: list) -> int:
        return len(cleaned_file)

    def fill_matrix(self, unique_words, counter):
        for word in unique_words:
            if word not in self.matrix:
                # If the word is not in the matrix, initialize a list of zeros
                self.matrix[word] = [0] * self.file_number
            # Update the list to indicate the presence of the word in the current file
            self.matrix[word][counter - 1] = 1

    def fill_inverted_index(self, unique_words, counter):
        for word in unique_words:
            if word not in self.inverted_index:
                self.inverted_index[word] = []

            if counter not in self.inverted_index[word]:
                self.inverted_index[word].append(counter)

    def save_matrix(self, output_file="../lab02/matrix.txt"):
        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame.from_dict(self.matrix, orient='index', columns=[f"Text{i + 1}" for i in range(self.file_number)])

        # Save the DataFrame
        with open(output_file, "w") as file:
            file.write(df.to_string())

        # df.to_csv(output_file, sep='\t', encoding='utf-8')

    def save_inverted_index(self, output_file="../lab02/inverted-index.txt"):
        with open(output_file, "w") as file:
            for key, value in self.inverted_index.items():
                value = " -> ".join(map(str, value))
                file.write(f"{key}\t {value}\n")

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Unique words: {len(self.collection)}")

    def save_result(self, output_file="results.txt"):
        with open(output_file, "w") as file:
            for word in self.collection:
                file.write(word + '\n')
