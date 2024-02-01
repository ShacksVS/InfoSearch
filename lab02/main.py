from processor import TextProcessor

if __name__ == "__main__":
    text_processor = TextProcessor()
    text_processor.process_files()
    text_processor.save_matrix()
    text_processor.print_summary()
