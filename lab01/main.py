from processor import TextProcessor
from utils import write_result

if __name__ == "__main__":
    file_paths = [f"../resources/text{i}.txt" for i in range(1, 11)]
    text_processor = TextProcessor()
    text_processor.process_files(file_paths)
    text_processor.print_summary()
    write_result(str(text_processor.collection))
