import re
import os
import time


class CoordIndex:
    def __init__(self, pattern=r"[^a-zA-Zа-яА-ЯіІїЇЮюҐ'’-]", stop_words=None):
        self.PATTERN = pattern
        self.file_number = 10
        self.total_kb = 0
        self.total_words = 0
        self.file_paths = [f"../resources/text{i + 1}.txt" for i in range(0, self.file_number)]
        self.coord_index_size = 0
        self.coord_dict = dict()
        self.stop_words = set(stop_words if stop_words else [])

    def process_files(self):
        file_counter = 1

        for file_path in self.file_paths:

            cleaned_words = self.clean_file(file_path)
            words_in_file = self.count_words_in_file(cleaned_words)

            self.fill_coord_index(cleaned_words, file_counter)
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

    def fill_coord_index(self, words, counter):
        for position, word in enumerate(words):
            if word not in self.coord_dict:
                self.coord_dict[word] = {}

            if counter not in self.coord_dict[word]:
                self.coord_dict[word][counter] = []

            self.coord_dict[word][counter].append(position + 1)

    def save_dict(self, output_file="../lab03/texts/coord-index.txt"):
        with open(output_file, "w") as file:
            for key, doc_positions in self.coord_dict.items():
                doc_positions_str = ' -> '.join([f"{doc_id} [{', '.join(map(str, positions))}]" for doc_id, positions in doc_positions.items()])
                file.write(f"{key}\t {doc_positions_str}\n")
        self.coord_index_size = os.path.getsize(output_file)

    def print_summary(self):
        print(f"Total KB in all files: {self.total_kb / 1000}")
        print(f"Total words in all files: {self.total_words}")
        print(f"Two words index size: {self.coord_index_size / 1000} KB")

    def simple_search(self, words: str):
        first_word, second_word = words.split(" ")
        print(first_word, second_word)

        start_time = time.time()
        found_first = self.coord_dict[first_word]
        found_second = self.coord_dict[second_word]

        sequence_found = {}

        # Iterate through all unique doc_ids present in either found_first or found_second
        all_docs = set(found_first.keys()).union(found_second.keys())
        
        for doc_id in all_docs:

            # Check if doc_id is present in both found_first and found_second
            if doc_id in found_first and doc_id in found_second:
                first_positions = found_first[doc_id]

                second_positions = found_second[doc_id]
                # Look for positions in first_positions where the next position is in second_positions
                sequence_positions = [(pos, pos + 1) for pos in first_positions if pos + 1 in second_positions]

                if sequence_positions:
                    sequence_found[doc_id] = sequence_positions

        found_time = (time.time() - start_time) * 1000  # convert to milliseconds

        print(f"\nFound '{first_word} {second_word}'"
              f"\nin {sequence_found}"
              f"\n\tin {found_time}")

    def coord_search(self, word: str):
        pass
