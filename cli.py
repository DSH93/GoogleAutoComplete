from bin.utils.DP import DataParser
from bin.Completer import SentenceCompleter
import threading
import time
import pickle
import os
import argparse
import logging
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'bin'))


compliter = None


def background_loading(data_parser):
    global compliter
    logging.info("Starting background loading...")
    start_time = time.time()

    lines = data_parser.get_lines()
    compliter = SentenceCompleter()

    for sentence, filename, offset in lines:
        compliter.add_sentence(sentence, filename, offset)

    end_time = time.time()
    logging.info(f"Data parsed in {end_time - start_time:.2f} seconds")


def load_data(data_path):
    if os.path.exists('completer.pkl'):
        with open('completer.pkl', 'rb') as f:
            data_parser = pickle.load(f)
        logging.info("Loaded completer from pickle file.")
    else:
        start_time = time.time()
        data_parser = DataParser(data_path)
        end_time = time.time()
        logging.info(f"Data loaded in {end_time - start_time:.2f} seconds")

    return data_parser


def main(data_path):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'bin'))
    if not os.path.exists(data_path):
        logging.error("Data path does not exist. Exiting.")
        return
    global compliter

    data_parser = load_data(data_path)

    # Start background data loading
    loading_thread = threading.Thread(
        target=background_loading, args=(data_parser,))
    loading_thread.start()

    input_phrase = ""
    loading_thread.join()
    logging.info("Completion data initialized.")

    input_phrase = ""
    print("Please enter a string (type '#' to stop current line, type '##' to stop): ")

    while True:
        input_phrase += " " + input(f"{input_phrase}")
        if '#' in input_phrase:
            input_phrase = input("Enter new phrase: ")
        elif '##' in input_phrase:
            break
        for index, sentence_data in enumerate(compliter.get_best_k_completions(input_phrase)):
            print(f"{index}. {str(sentence_data)}")
        else:
            logging.error("Completion data was not initialized.")

    with open('completer.pkl', 'wb') as f:
        pickle.dump(data_parser, f)
    logging.info("Completer state saved to 'completer.pkl'.")


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="CLI for Sentence Completion")
    parser.add_argument("-d", "--data", type=str, required=True,
                        help="Path to the directory containing the data files")
    args = parser.parse_args()

    # Ensure the log directory exists
    log_dir = "bin/log"
    os.makedirs(log_dir, exist_ok=True)

    # Set up logging to only file in bin/log
    log_file_path = os.path.join(log_dir, "completer.log")
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[
                            logging.FileHandler(log_file_path)
                        ])
    main(args.data)
