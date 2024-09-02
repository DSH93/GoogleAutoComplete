import Levenshtein

def calculate_custom_score(input_word, word):
    # Calculate the Levenshtein distance between the input word and the current word
    distance = Levenshtein.distance(input_word, word)
    operations = Levenshtein.editops(input_word, word)
    punishment = 0
    max_score = len(input_word) * 2

    if distance > 1:
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



def rank_candidates(input_word, word_list):
    scored_words = [(word, calculate_custom_score(input_word, word)) for word in word_list]
    scored_words.sort(key=lambda x: x[1], reverse=True)
    return scored_words[:10]

def sentence_with_specific_word(word_sentence_map, top_10_words, input_word):
    sentences = []
    for word, score in top_10_words:
        if score > len(input_word) * (-10):
            print(f"Word: {word}")
            print(f"Score: {score}")
            print(f"Sentences:")
            for sentence in word_sentence_map[word]:
                print(sentence)
                print()
                sentences.append(sentence)
    return sentences