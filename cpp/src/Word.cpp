//
// Created by Dor Shukrun on 14/09/2024.
//

#include "../include/Word.h"
#include <utility>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>

// EditOperation struct definition
struct EditOperation {
    char type;  // 'i' for insert, 'd' for delete, 'r' for replace
    size_t index_s1;  // index in s1 where the operation occurred
    size_t index_s2;  // index in s2 where the operation occurred
};

int min(int a, int b, int c);

int levenshteinDistance(const std::string &s1, const std::string &s2, std::vector<EditOperation> &operations);

// Destructor
Word::~Word() = default;

// Getters
std::string Word::getWord() {
    return word;
}

int Word::getScore() const {
    return score;
}

int Word::getMaxScore() const {
    return maxScore;
}

float Word::getAccuracy() const {
    if (maxScore == 0) return 0;
    return static_cast<float>(score) / maxScore;
}

int Word::getFrequency() const {
    return frequency;
}

// Setters
void Word::setScore(int score1) {
    this->score = score1;
}

void Word::setMaxScore(int maxScore1) {
    this->maxScore = maxScore1;
}

void Word::setAccuracy(float accuracy1) {
    this->accuracy = accuracy1;
}

void Word::setFrequency(int frequency1) {
    this->frequency = frequency1;
}

void Word::setUserInput(std::string userInp) {
    this->userInput = std::move(userInp);
}

// Calculate score based on Levenshtein distance
void Word::calculateScore() {
    std::vector<EditOperation> operations;

    std::string word1 = getWord();
    int distance = levenshteinDistance(userInput, word1, operations);
    int max_score = userInput.length() * 2;
    int punishment = 0;




    for (const auto &op: operations) {
        int index = op.index_s2;
        if (op.type == 'r') {  // replace
            punishment += -1 * std::max(1, 5 - index);
        } else if (op.type == 'i') {  // insert
            punishment += -2 * std::max(1, 5 - index);
        } else if (op.type == 'd') {  // delete
            punishment += -2 * std::max(1, 5 - index);
        }
    }
    int totalScore = max_score + punishment;
    setScore(totalScore);
    setMaxScore(max_score);
    setAccuracy(getAccuracy());
}

// Get word and its score as a string
std::string Word::getWordAndScore() {
    return word + " [Score: <" + std::to_string(score) + ">]";
}

// Levenshtein distance calculation with operation tracking
int levenshteinDistance(const std::string &s1, const std::string &s2, std::vector<EditOperation> &operations) {
    const size_t len1 = s1.size(), len2 = s2.size();
    std::vector<std::vector<int>> d(len1 + 1, std::vector<int>(len2 + 1));
    for (size_t i = 0; i <= len1; ++i) d[i][0] = i;
    for (size_t j = 0; j <= len2; ++j) d[0][j] = j;

    // Compute distance matrix
    for (size_t i = 1; i <= len1; ++i) {
        for (size_t j = 1; j <= len2; ++j) {
            int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
            d[i][j] = std::min({
                                       d[i - 1][j] + 1,        // deletion
                                       d[i][j - 1] + 1,        // insertion
                                       d[i - 1][j - 1] + cost  // substitution or match
                               });
        }
    }

    size_t i = len1;
    size_t j = len2;

    while (i > 0 || j > 0) {
        if (i > 0 && d[i][j] == d[i - 1][j] + 1) {
            operations.push_back({'d', i - 1, j});
            i--;
        } else if (j > 0 && d[i][j] == d[i][j - 1] + 1) {
            operations.push_back({'i', i, j - 1});
            j--;
        } else if (i > 0 && j > 0) {
            int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
            if (d[i][j] == d[i - 1][j - 1] + cost) {
                if (cost == 1) {
                    operations.push_back({'r', i - 1, j - 1});
                }
                i--;
                j--;
            }
        } else {
            break;
        }
    }


    std::reverse(operations.begin(), operations.end());
    return d[len1][len2];
}

bool Word::operator<(const Word &word) const {
    return accuracy < word.accuracy;
}

