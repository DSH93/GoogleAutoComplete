from data_processing import read_sentences_from_files, create_word_sentence_map
from bin.utils.Scorer import rank_candidates, sentence_with_specific_word
from collections import Counter

def words_in_sequence(words, sentence):
    """
    Check if all words appear in sequence within the sentence.
    """
    sentence_words = sentence.split()
    sentence_str = ' '.join(sentence_words)
    phrase = ' '.join(words)
    
    return phrase in sentence_str

if __name__ == "__main__":
    directory_path = r"C:\Users\Dor Shukrun\Desktop\Exelanteem\mvp data"
    all_sentences = read_sentences_from_files(directory_path)
    word_sentence_map = create_word_sentence_map(all_sentences)
    
    word_list = list(word_sentence_map.keys())

    # Count frequencies of each word
    word_frequencies = Counter(word_list)

    # Ask the user to input one or more words
    input_phrase = input("Enter one or more words: ").strip().lower()

    # Split the input into individual words
    input_words = input_phrase.split()

    # Variable to store the intersection of sentences
    common_sentences = None
    common_words_and_sentences = []

    # Process each word individually
    for input_word in input_words:
        top_10_words = rank_candidates(input_word, word_list)
        result = sentence_with_specific_word(word_sentence_map, top_10_words, input_word)
        
        # Convert the result into a set of sentences for easier intersection
        current_sentences = set(sentence[1] for sentence in result)
        
        if common_sentences is None:
            # Initialize the common sentences with the first set of sentences
            common_sentences = current_sentences
            common_words_and_sentences = result
        else:
            # Perform intersection to keep only common sentences
            common_sentences &= current_sentences
            
            # Keep only the sentences that are common across all words
            common_words_and_sentences = [
                (word_score, sentence) for word_score, sentence in common_words_and_sentences 
                if sentence in common_sentences
            ]

    # Print the results in the required format
    if common_words_and_sentences:
        for word_score, sentence in common_words_and_sentences:
            # Check if all words appear in sequence in the sentence
            if words_in_sequence(input_words, sentence):
                print(f"{word_score}, '{sentence}'")
                print()
    else:
        print("No common sentences found for the given words.")
