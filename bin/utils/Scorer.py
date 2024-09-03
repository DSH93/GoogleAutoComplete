import Levenshtein


def is_valid_substring(input_word: str, candidate_word: str) -> bool:
    # Checks if the candidate word is a valid substring of the input word
    len_input = len(input_word)
    for i in range(len(candidate_word) - len_input + 1):
        substring = candidate_word[i:i + len_input]
        distance = Levenshtein.distance(input_word, substring)
        if distance == 1:
            if input_word[0] != substring[0] and input_word[1:] == substring[1:]:
                if i == 0 or candidate_word[i-1].isspace():
                    if i + len_input == len(candidate_word) or candidate_word[i + len_input].isspace():
                        return True
        elif distance == 0:
            return True
    return False


def calculate_custom_score(input_word: str, word: str) -> int:
    # Scores the word based on the input word first of all max scoring given and then punishment is given based on the operations
    distance = Levenshtein.distance(input_word, word)
    operations = Levenshtein.editops(input_word, word)
    punishment = 0
    max_score = len(input_word) * 2
    if distance > 1 and not is_valid_substring(input_word, word):
        print(f"Input word {input_word} | word {word} | distance {distance} | operations {operations} | punishment {punishment}")
        return max_score * (-10)
    for i in range(len(operations)):
        index = operations[i][1]
        if operations[i][0] == 'replace':
            punishment += -1 * max(1, 5 - index)
        elif operations[i][0] == 'insert':
            punishment += -2 * max(1, 5 - index)
        elif operations[i][0] == 'delete':
            punishment += -2 * max(1, 5 - index)
    score = max_score + punishment
    return score
