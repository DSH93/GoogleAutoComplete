//
// Created by Dor Shukrun on 13/09/2024.
//

#include "../include/Score.h"
#include <algorithm>
#include <vector>
#include <iostream>


int WordScorer::levenshteinDistance(const std::string& s1, const std::string& s2) {
    const size_t len1 = s1.size(), len2 = s2.size();
    std::vector<std::vector<int>> d(len1 + 1, std::vector<int>(len2 + 1));

    for (size_t i = 0; i <= len1; ++i) d[i][0] = i;
    for (size_t i = 0; i <= len2; ++i) d[0][i] = i;

    for (size_t i = 1; i <= len1; ++i)
        for (size_t j = 1; j <= len2; ++j)
            d[i][j] = std::min({d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (s1[i - 1] == s2[j - 1] ? 0 : 1)});

    return d[len1][len2];
}


std::vector<WordScorer::EditOperation> WordScorer::editOperations(const std::string& s1, const std::string& s2) {
    std::vector<EditOperation> operations;
    return operations;
}


bool WordScorer::isValidSubstring(const std::string& inputWord, const std::string& candidateWord) {
    size_t len_input = inputWord.size();
    for (size_t i = 0; i <= candidateWord.size() - len_input; ++i) {
        std::string substring = candidateWord.substr(i, len_input);
        int distance = levenshteinDistance(inputWord, substring);
        if (distance == 1) {
            if (inputWord[0] != substring[0] && inputWord.substr(1) == substring.substr(1)) {
                if (i == 0 || std::isspace(candidateWord[i - 1])) {
                    if (i + len_input == candidateWord.size() || std::isspace(candidateWord[i + len_input])) {
                        return true;
                    }
                }
            }
        } else if (distance == 0) {
            return true;
        }
    }
    return false;
}


int WordScorer::calculateCustomScore(const std::string& inputWord, const std::string& word) {
    int distance = levenshteinDistance(inputWord, word);
    std::vector<EditOperation> operations = editOperations(inputWord, word);
    int punishment = 0;
    int max_score = inputWord.length() * 2;



    for (const auto& op : operations) {
        int index = op.index;
        if (op.type == 'r') {  // replace
            punishment += -1 * std::max(1, 5 - index);
        } else if (op.type == 'i') {  // insert
            punishment += -2 * std::max(1, 5 - index);
        } else if (op.type == 'd') {  // delete
            punishment += -2 * std::max(1, 5 - index);
        }
    }

    int score = max_score + punishment;
    return score;
}
