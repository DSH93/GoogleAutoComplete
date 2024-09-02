import os
import re
from collections import defaultdict

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
        words = set(sentence.split())  
        for word in words:
            word_sentence_map[word].append(sentence)
    
    return word_sentence_map
