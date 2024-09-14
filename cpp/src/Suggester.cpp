//
// Created by Dor Shukrun on 13/09/2024.
//

#include "../include/Suggester.h"

Suggester::Suggester(std::string path) {
    DataParser dataParser(path);
    wordToSentence = std::move(dataParser.getWordToSentence());
    wordsCountAndLength = std::move(dataParser.getWordsCountAndLength());
}

Suggester::~Suggester() = default;
