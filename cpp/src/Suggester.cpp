//
// Created by Dor Shukrun on 13/09/2024.
//

#include <algorithm>
#include "../include/Suggester.h"


Suggester::Suggester(const std::string& path) {
    DataParser dataParser(path);
    wordToSentence = dataParser.getWordToSentence();
    wordsCountByLength = dataParser.getWordsCountAndLength();
}

void Suggester::suggest() {
    std::string userInput;
    std::cout << "Enter a word: ";
    std::cin >> userInput;
    std::vector<Word> words = getHighestScoreWords(userInput);

    std::sort(words.begin(), words.end(), [](const Word& a, const Word& b) {
        return a.getScore() > b.getScore();
    });


    int topSuggestions = 10;
    for (auto& word : words) {
        if (topSuggestions == 0) break;
        const auto& sentences = wordToSentence[word.getWord()];
        for (const auto& sentence : sentences) {
            if (topSuggestions == 0) break;
            topSuggestions--;
            std::cout << word.getWord() << " [acc:" << word.getAccuracy() << "]" << sentence << std::endl;
        }
    }


}



std::vector<std::pair<std::string, int>> Suggester::getWordsByLength(int length) {
    if (wordsCountByLength.find(length) != wordsCountByLength.end()) {
        return wordsCountByLength[length];
    }
    return {};
}

void Suggester::addWord(const std::string& word, int frequency) {
    int length = word.length();
    wordsCountByLength[length].emplace_back(word, frequency);
}




std::vector<Word> Suggester::getHighestScoreWords(const std::string& userInput) {
    std::vector<Word> words;
    unsigned int userInputLength = userInput.length();
    int errorRadius = 1;


    auto processWordsByLength = [&](int length) {
        auto wordsByLength = getWordsByLength(length);
        for (const auto& pair : wordsByLength) {
            const std::string& wordStr = pair.first;
            int frequency = pair.second;

            Word w(wordStr);
            w.setFrequency(frequency);
            w.setUserInput(userInput);
            w.calculateScore();
            words.push_back(w);
        }
    };

    processWordsByLength(userInputLength);
    processWordsByLength(userInputLength + errorRadius);
    if (userInputLength > errorRadius) {
        processWordsByLength(userInputLength - errorRadius);
    }

    return words;
}


Suggester::~Suggester() = default;
