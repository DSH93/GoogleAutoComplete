import Levenshtein

def is_valid_substring(input_word, candidate_word):
    len_input = len(input_word)
    for i in range(len(candidate_word) - len_input + 1):
        substring = candidate_word[i:i + len_input]
        distance = Levenshtein.distance(input_word, substring)
        
        if distance == 1:
            # אם יש טעות אחת, נוודא שכל תת המחרוזת התואמת היא לחלוטין פרט לטעות אחת
            if input_word[0] != substring[0] and input_word[1:] == substring[1:]:
                # נבדוק גם שאין תווים נוספים לפני או אחרי תת-המחרוזת שיכולים להשפיע
                if i == 0 or candidate_word[i-1].isspace():
                    if i + len_input == len(candidate_word) or candidate_word[i + len_input].isspace():
                        return True
        elif distance == 0:
            # אם כל תת-המחרוזת תואמת לחלוטין, המחרוזת תקינה
            return True

    return False


def calculate_custom_score(input_word, word):
    distance = Levenshtein.distance(input_word, word)
    operations = Levenshtein.editops(input_word, word)
    punishment = 0
    max_score = len(input_word) * 2

    
    
    if distance > 1 and not is_valid_substring(input_word, word):
        
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
        if score > len(input_word) * (-10):  # מוודא שרק מילים עם ניקוד חיובי יופיעו
            for sentence in word_sentence_map[word]:
                words_and_sentence = [(word, score), sentence]
                sentences.append(words_and_sentence)
    return sentences
