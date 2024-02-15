from two_words_index import TwoWordsIndex
from coord_index import CoordIndex


if __name__ == "__main__":
    # stop_words = ["і", "на", "у", "в", "а", "з", "зі", "до"]
    # words_index = TwoWordsIndex(stop_words=stop_words)
    # words_index.process_files()
    # words_index.find("побував своїм")

    coord_index = CoordIndex()
    coord_index.process_files()
    # coord_index.simple_search("моринці київської")
    # coord_index.simple_search("родині селянина-кріпака")
    coord_index.simple_search("князівська династія")
