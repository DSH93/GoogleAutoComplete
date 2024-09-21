//
// Created by Dor Shukrun on 13/09/2024.
//

#ifndef CPP_SUGGESTER_H
#define CPP_SUGGESTER_H


#include <iostream>
#include "DataParser.h"
#include "Word.h"
#include <string>

class Suggester {
private:

    std::unordered_map<int, std::vector<std::pair<std::string, int>>> wordsCountByLength;
    std::unordered_map<std::string, std::vector<std::string>> wordToSentence;
    std::vector<Word> getHighestScoreWords(const std::string& userInput);

public:
    Suggester(const std::string& path);
    ~Suggester();
    void suggest();
    std::vector<std::pair<std::string, int>> getWordsByLength(int length);
    void addWord(const std::string &word, int frequency);
};


#endif //CPP_SUGGESTER_H
