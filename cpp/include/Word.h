//
// Created by Dor Shukrun on 14/09/2024.
//

#ifndef CPP_WORD_H
#define CPP_WORD_H


#include <string>
#include <unordered_map>
#include <utility>

class Word {
private:
    std::string word;
    std::string userInput;
    int score;
    int maxScore;
    float accuracy;
    int frequency;

public:
    Word(std::string word, int score, int maxScore, float accuracy, int frequency) : word(std::move(word)),userInput(userInput), score(score), maxScore(maxScore), accuracy(accuracy), frequency(frequency) {}
    explicit Word(const std::string& word) : word(word), userInput(), score(0), maxScore(0), accuracy(0.0f), frequency(0) {}
    ~Word();
    std::string getWord();
    std::string getWordAndScore();
    int getScore() const;
    int getMaxScore() const;
    float getAccuracy() const;
    int getFrequency() const;
    void setScore(int score1);
    void setMaxScore(int maxScore1);
    void setAccuracy(float accuracy1);
    void setFrequency(int frequency1);
    void setUserInput(std::string userInp);
    void calculateScore();
    bool operator<(const Word& word) const;




};


#endif //CPP_WORD_H
