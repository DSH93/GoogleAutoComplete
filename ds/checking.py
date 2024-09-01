import os
import re
from collections import defaultdict, Counter

def read_sentences_from_files(directory_path):
    sentences = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):  
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Convert to lowercase and remove non-alphabetic characters
                content = re.sub(r'[^a-zA-Z\s\.\!\?]', '', content.lower())
                
                # Split sentences based on period, exclamation mark, and question mark
                raw_sentences = re.split(r'[.!?]', content)
                
                for sentence in raw_sentences:
                    clean_sentence = re.sub(r'\s+', ' ', sentence.strip())  # Remove extra spaces and tabs
                    if len(clean_sentence.split()) >= 2:  # Ensure the sentence has at least 2 words
                        sentences.append(clean_sentence)  # Store the sentence as a string
    
    return sentences

def create_word_sentence_map(sentences):
    word_sentence_map = defaultdict(list)
    
    for sentence in sentences:
        words = set(sentence.split())  # Use set to avoid duplicating the same sentence for a word
        for word in words:
            word_sentence_map[word].append(sentence)
    
    return word_sentence_map

def calculate_similarity_score(input_word, candidate_word, word_frequencies):
    # Calculate frequency score based on letter frequency in candidate word
    input_word_letter_count = Counter(input_word)
    candidate_word_letter_count = Counter(candidate_word)

    # Calculate letter frequency similarity
    common_letters = sum(min(input_word_letter_count[char], candidate_word_letter_count[char]) for char in input_word_letter_count)
    
    # Calculate order similarity
    order_similarity = sum(1 for a, b in zip(input_word, candidate_word) if a == b)

    # Final score is a combination of letter frequency and order similarity
    score = common_letters + order_similarity
    
    # Adjust score by word frequency
    score *= word_frequencies[candidate_word]

    return score

def find_closest_word(input_word, word_list, word_frequencies):
    # Initialize variables to track the best word and highest score
    best_word = None
    highest_score = 0

    # Iterate over each word in the word list
    for word in word_list:
        # Calculate the similarity score for each word
        score = calculate_similarity_score(input_word, word, word_frequencies)
        
        # If the current word has a higher score, or if it's a tie and it occurs more frequently, update best_word
        if score > highest_score or (score == highest_score and word_frequencies[word] > word_frequencies[best_word]):
            best_word = word
            highest_score = score

    return best_word

if __name__ == "__main__":
    directory_path = r"C:\Users\Dor Shukrun\Desktop\Exelanteem\mvp data"

    # Read sentences from files
    all_sentences = read_sentences_from_files(directory_path)

    # Create word-sentence map
    word_sentence_map = create_word_sentence_map(all_sentences)
    
    # Create a list of all unique words from the word-sentence map
    word_list = list(word_sentence_map.keys())

    # Count frequencies of each word
    word_frequencies = Counter(word_list)

    # Ask the user to input a word
    input_word = input("Enter a word: ").strip().lower()

    # Find the closest word in the dataset
    closest_word = find_closest_word(input_word, word_list, word_frequencies)
    
    # Print the sentences containing the closest word
    if closest_word in word_sentence_map:
        print(f"Closest word found: '{closest_word}'")
        print(f"Sentences containing the word '{closest_word}':")
        for sentence in word_sentence_map[closest_word]:
            print(sentence)
            print()  # Add an empty line for better readability
    else:
        print(f"No sentences found containing the word '{closest_word}'.")
