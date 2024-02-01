import re
import os


class TextProcessor:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-Я'’-]"):
        self.pattern = pattern
        self.collection = set()
        self.total_kb = 0
        self.total_words = 0

    def normalize_text(self, text):
        return re.sub(self.pattern, ' ', text).lower()

    def normalize_file(self, file_path: str):
        with open(file_path, "r") as my_file:
            normalized_words = self.normalize_text(my_file.read()).split()
            words = len(normalized_words)
            return set(normalized_words), words

    def process_files(self, file_paths):
        for file_path in file_paths:
            unique_words, words_in_file = self.normalize_file(file_path)
            self.collection.update(unique_words)
            self.total_words += words_in_file
            self.total_kb += os.path.getsize(file_path)

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Unique words: {len(self.collection)}")