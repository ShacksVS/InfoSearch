def write_result(collection: str, output_file="results.txt"):
    with open(output_file, "w") as file:
        file.write(collection)