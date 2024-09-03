from collections import defaultdict
from bin.utils.Scorer import calculate_custom_score
from bin.utils.Enum import AutoCompleteData, TreeNode


class Tree:
    """ 
        A tree data structure to store the sentences, constructed from the words in the sentences.
        Each node in the tree represents a character in a word. The children of a node are the characters that 
        follow the current character in a word.The indices list in a node stores the indices of the sentences 
        that contain the word represented by the path from the root to the node.
    """
    def __init__(self):
        self.root = TreeNode()

    def insert(self, sentence, index):
        words = sentence.lower().split()
        for word in words:
            current = self.root
            for char in word:
                if char not in current.children:
                    current.children[char] = TreeNode()
                current = current.children[char]
            current.indices.append(index)
            current.word = word

    def search(self, word):
        word = word.lower()
        results = self._search_recursive(self.root, word, "")
        results.sort(key=lambda x: x[0], reverse=True)
        return results

    # Recursive function to search for a word in the tree, starting from a given node.
    # Returns a list of tuples containing the score and the indices of the sentences that contain the word.
    def _search_recursive(self, node, word, current_word):
        results = []

        if len(current_word) > len(word): 
            return results

        if node.word:
            score = calculate_custom_score(word, current_word)
            results.append((score, node.indices))

        if len(current_word) < len(word):
            next_char = word[len(current_word)]
            if next_char in node.children:
                results.extend(self._search_recursive(
                    node.children[next_char], word, current_word + next_char))

        return results


class SentenceCompleter:
    def __init__(self):
        self.tree = Tree()
        self.sentences = defaultdict(dict)
        self.index = 0

    def add_sentence(self, sentence, filename, offset):
        self.sentences[self.index] = {
            'sentence': sentence, 'offset': offset, 'filename': filename}
        self.tree.insert(sentence, self.index)
        self.index += 1

    def get_best_k_completions(self, prefix:str) -> list[AutoCompleteData]:
        input_words = prefix.lower().split()
        if not input_words:
            return []

        all_candidate_indices = []
        for word in input_words:
            search_results = self.tree.search(word)
            if not search_results:
                return []
            all_candidate_indices.append(search_results)

        scored_sentences = []
        for score, candidate_list in all_candidate_indices[0]:
            for index in candidate_list:
                sentence_data = self.sentences[index]
                words_in_sentence = sentence_data['sentence'].lower().split()

                if self._words_in_order(words_in_sentence, input_words):
                    total_score = sum(calculate_custom_score(input_word, w)
                                      for input_word, w in zip(input_words, words_in_sentence))
                    new_data_entry = AutoCompleteData(completed_sentence=sentence_data['sentence'],
                                                      source_text=sentence_data['filename'],
                                                      offset=sentence_data['offset'],
                                                      score=total_score)
                    scored_sentences.append(new_data_entry)

        # Sort by score (higher score is better)
        scored_sentences.sort(key=lambda x: x.score)

        # Return the top 5 matches with the highest score
        return scored_sentences[-5:]

    def _words_in_order(self, words_in_sentence, input_words):
        """Check if input_words are in the correct order within words_in_sentence."""
        word_idx = 0
        for word in words_in_sentence:
            if word_idx < len(input_words) and calculate_custom_score(input_words[word_idx], word) > 0:
                word_idx += 1
            if word_idx == len(input_words):
                return True
        return False
