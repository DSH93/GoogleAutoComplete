from collections import defaultdict
from bin.utils.Scorer import calculate_custom_score
from bin.utils.Enum import AutoCompleteData
from bin.ds.Tree import Tree


class SentenceCompleter:
    """
        Main program, that proposes completions. Makes main use of Tree with Hash Map
        Tree is used to store the sentences and Hash map storing the indices of the sentences
        Main function is get_best_k_completions that returns the best 5 completions for a given
        prefix of a sentence based on the score that prefix gets
    """

    def __init__(self):
        self.tree = Tree()
        self.sentences = defaultdict(dict)
        self.index = 0

    def add_sentence(self, sentence, filename, offset):
        # add new entry to the tree and hash map
        self.sentences[self.index] = {
            'sentence': sentence, 'offset': offset, 'filename': filename}
        self.tree.insert(sentence, self.index)
        self.index += 1

    def get_best_k_completions(self, prefix: str) -> list[AutoCompleteData]:
        # get best 5 complitions
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
        # run through all candidates and check if the words are in order and calculate the score
        for _, candidate_list in (all_candidate_indices[0]):
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
        return scored_sentences[-5:]

    def _words_in_order(self, words_in_sentence, input_words):
        # Check if input_words are in the correct order within words_in_sentence.
        word_idx = 0
        for word in words_in_sentence:
            if word_idx < len(input_words) and calculate_custom_score(input_words[word_idx], word) > 0:
                word_idx += 1
            if word_idx == len(input_words):
                return True
        return False
