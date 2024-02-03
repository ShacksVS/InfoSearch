from processor import TextProcessor


if __name__ == "__main__":
    text_processor = TextProcessor()
    text_processor.process_files()

    running = True

    while running:
        # prompt = input("-> ")
        # prompt = "київської AND в"
        prompt = "not моринці"
        if prompt == "q":
            break

        lst_prompt = prompt.lower().split()

        if lst_prompt[1] == "and":
            text_processor.handle_and_operator(lst_prompt)
        elif lst_prompt[1] == "or":
            text_processor.handle_or_operator(lst_prompt)
        elif lst_prompt[0] == "not":
            text_processor.handle_not_operator(lst_prompt)
        else:
            print("Unexpected input")

        running = False
