import re
import os
import time


class TwoWordsIndex:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]", stop_words=None):
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.two_words_index_size = 0
        self.two_words_dict = dict()
        self.stop_words = set(stop_words if stop_words else [])

    def process_files(self):
        file_counter = 1

        for file_path in self.file_paths:

            cleaned_words = self.clean_file(file_path)
            words_in_file = self.count_words_in_file(cleaned_words)

            self.fill_two_words_index(cleaned_words, file_counter)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

            print(f"Done with {file_counter}")
            file_counter += 1

        self.save_dict()
        # self.print_summary()

    def normalize_text(self, text):
        return re.sub(self.PATTERN, ' ', text).lower()

    def clean_file(self, file_path: str):
        with open(file_path, "r") as my_file:
            words = self.normalize_text(my_file.read()).split()
            return [word for word in words if word not in self.stop_words]

    def count_words_in_file(self, cleaned_file: list) -> int:
            return len(cleaned_file)

    def fill_two_words_index(self, words, counter):
        for i in range(len(words) - 1):
            two_word_pair = f"{words[i]} {words[i + 1]}"
            if two_word_pair not in self.two_words_dict:
                self.two_words_dict[two_word_pair] = []

            if counter not in self.two_words_dict[two_word_pair]:
                self.two_words_dict[two_word_pair].append(counter)

    def save_dict(self, output_file="../lab03/texts/two-words-index.txt"):
        with open(output_file, "w") as file:
            for key, value in self.two_words_dict.items():
                value = " -> ".join(map(str, value))
                file.write(f"{key}\t {value}\n")
        self.two_words_index_size = os.path.getsize(output_file)

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Two words index size: {self.two_words_index_size / 1000} KB")


    def find(self, words: str):
        start_time = time.time()
        found = self.two_words_dict[words]
        found_time = (time.time() - start_time) * 1000  # convert to milliseconds

        print(f"\nFound '{words}' in {found}"
              f"\n\tin {found_time}")