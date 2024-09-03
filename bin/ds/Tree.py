from bin.utils.Enum import TreeNode


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
