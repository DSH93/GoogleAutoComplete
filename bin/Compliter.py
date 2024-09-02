import os
from collections import defaultdict
import Levenshtein as lev
import os
from string import punctuation
from utils.DP import DataParser
import pickle


class TreeNode:
    def __init__(self):
        self.children = {}
        self.indices = []
        self.word = None


class Tree:
    def __init__(self):
        self.root = TreeNode()

    def insert(self, sentence, index):
        # Convert sentence to lowercase for case insensitivity
        words = sentence.lower().split()
        for word in words:
            current = self.root
            for char in word:
                if char not in current.children:
                    current.children[char] = TreeNode()
                current = current.children[char]
            current.indices.append(index)
            current.word = word

    def search(self, word, max_distance=1):
        """Searches for words in the trie that are within a given Levenshtein distance."""
        word = word.lower()
        return self._search_recursive(self.root, word, "", max_distance, [])

    def _search_recursive(self, node, word, current_word, max_distance, results):
        distance = lev.distance(word, current_word)
        if distance <= max_distance and node.word:
            results.append((current_word, node.indices))

        if len(current_word) < len(word) + max_distance:
            for char, child_node in node.children.items():
                self._search_recursive(
                    child_node, word, current_word + char, max_distance, results)

        return results


class SentenceCompleter:
    def __init__(self):
        self.tree = Tree()
        self.sentences = defaultdict(dict)
        self.index = 0

    def add_sentence(self, sentence, filename,  offset):
        self.sentences[self.index] = {
            'sentence': sentence, 'offset': offset, 'filename': filename}
        self.tree.insert(sentence, self.index)
        self.index += 1

    def complete(self, input_text):
        # Convert input to lowercase for case insensitivity
        input_words = input_text.lower().split()
        if not input_words:
            return []

        # Search for words in the trie that match the input with a maximum Levenshtein distance of 1
        all_candidate_indices = []
        for word in input_words:
            search_results = self.tree.search(word, max_distance=1)
            if not search_results:
                return []  # If any word doesn't match, return nothing
            all_candidate_indices.append(search_results)

        # Find sentences that contain all words in the correct order
        scored_sentences = []
        for word, candidate_list in all_candidate_indices[0]:
            for index in candidate_list:
                sentence_data = self.sentences[index]
                # Case insensitive comparison
                words_in_sentence = sentence_data['sentence'].lower().split()

                if self._words_in_order(words_in_sentence, input_words):
                    total_score = sum(self.calculate_custom_score(input_word, w)
                                      for input_word, w in zip(input_words, words_in_sentence))
                    scored_sentences.append((total_score, sentence_data))

        # Sort by score (lower score is better)
        scored_sentences.sort(key=lambda x: x[0])

        # Return the top 5 matches with the highest similarity (lowest score)
        return scored_sentences[:5]

    def _words_in_order(self, words_in_sentence, input_words):
        """Check if input_words are in the correct order within words_in_sentence."""
        word_idx = 0
        for word in words_in_sentence:
            if word_idx < len(input_words) and lev.distance(input_words[word_idx], word) <= 1:
                word_idx += 1
            if word_idx == len(input_words):
                return True
        return False

    def calculate_custom_score(self, input_word, matched_word):
        base_score = 2 * len(input_word)
        # Penalize based on Levenshtein distance
        penalty = lev.distance(input_word, matched_word) * 2
        return base_score - penalty


# Example usage:
completer = SentenceCompleter()
dataparser = DataParser('data/')
with open('data/DP.pkl', 'wb') as f:
    pickle.dump(dataparser, f)
for line in dataparser.get_sentences():
    completer.add_sentence(line[0], line[1], line[2])
# save the completer
print(f"Loaded {len(completer.sentences)}")
# Search for the word "introduction"
print("Trying suggestion")
suggestions = completer.complete("python code")
for score, sentence in suggestions:
    print(f"Score: {score}, Sentence: {sentence['sentence']}, Offset: {
          sentence['offset']}, Filename: {sentence['filename']}")
