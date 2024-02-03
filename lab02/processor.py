import re
import os
import time

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

    def handle_and_operator(self, prompt: list):
        first_word, second_word = prompt[0], prompt[2]

        print(f"Finding {first_word} AND {second_word}..")

        #
        # finding in matrix
        #

        start_time_matrix = time.time()

        found_files_in_matrix = self.matrix[first_word] or self.matrix[second_word]
        time_matrix = (time.time() - start_time_matrix) * 1000  # convert to milliseconds

        print(found_files_in_matrix, time_matrix)

        #
        # finding in inverted index
        #

        start_time_inverted = time.time()

        found_files_in_inverted = self.inverted_index[first_word] or self.inverted_index[second_word]
        time_inverted = (time.time() - start_time_inverted) * 1000  # convert to milliseconds

        print(found_files_in_inverted, time_inverted)

    def handle_or_operator(self, prompt):
        first_word, second_word = prompt[0], prompt[2]

        print(f"Finding {first_word} OR {second_word}..")

        #
        # finding in matrix
        #

        start_time_matrix = time.time()

        found_files_in_matrix = self.matrix[first_word] and self.matrix[second_word]
        time_matrix = (time.time() - start_time_matrix) * 1000  # convert to milliseconds

        print(found_files_in_matrix, time_matrix)

        #
        # finding in inverted index
        #

        start_time_inverted = time.time()

        found_files_in_inverted = self.inverted_index[first_word] and self.inverted_index[second_word]
        time_inverted = (time.time() - start_time_inverted) * 1000  # convert to milliseconds

        print(found_files_in_inverted, time_inverted)

    def handle_not_operator(self, prompt):
        not_word = prompt[1]
        print(f"Finding not {not_word}..")

        #
        # finding in matrix
        #

        start_time_matrix = time.time()

        if not_word in self.matrix:
            found_files_in_matrix = [0] * self.file_number

            for file_index, presence in enumerate(self.matrix[not_word]):
                found_files_in_matrix[file_index] = 0 if presence == 1 else 1

        else:
            print("Word is not in collection")
            return

        time_matrix = (time.time() - start_time_matrix) * 1000  # convert to milliseconds

        print(found_files_in_matrix, time_matrix)

        #
        # Finding in inverted index
        #

        start_time_inverted = time.time()
        all_files = set(range(1, self.file_number + 1))

        if not_word in self.inverted_index:
            found_files_in_inverted = set(self.inverted_index[not_word])
            found_files_in_inverted = all_files - found_files_in_inverted

        else:
            found_files_in_inverted = all_files

        time_inverted = (time.time() - start_time_inverted) * 1000  # Convert to milliseconds
        print(found_files_in_inverted, time_inverted)
