from data_processing import read_sentences_from_files, create_word_sentence_map
from scoring import rank_candidates, sentence_with_specific_word
from collections import Counter

if __name__ == "__main__":
    directory_path = r"C:\Users\Dor Shukrun\Desktop\Exelanteem\mvp data"
    all_sentences = read_sentences_from_files(directory_path)
    word_sentence_map = create_word_sentence_map(all_sentences)
    
    word_list = list(word_sentence_map.keys())

    # Count frequencies of each word
    word_frequencies = Counter(word_list)

    # Ask the user to input a word
    input_word = input("Enter a word: ").strip().lower()

    # Find the closest word in the dataset
    top_10_words = rank_candidates(input_word, word_list)
    
    sentence_with_specific_word(word_sentence_map, top_10_words, input_word)
    
    
