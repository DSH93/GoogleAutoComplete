//
// Created by Dor Shukrun on 13/09/2024.
//

#include "../include/Suggester.h"

Suggester::Suggester(std::string path) {
    DataParser dataParser(path);
    uniqueWords = dataParser.getWordsByMinHash(10);
    wordToSentence = dataParser.getWordToSentence();
}

Suggester::~Suggester() = default;