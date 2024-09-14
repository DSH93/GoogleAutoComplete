//
// Created by Dor Shukrun on 14/09/2024.
//

#ifndef CPP_WORD_H
#define CPP_WORD_H


#include <string>

class Word {
private:
    std::string word;
    int score;
    int maxScore;
    float accuracy;
    int frequency;

public:
    Word(std::string word, int score, int maxScore, float accuracy, int frequency);
    ~Word();
    std::string getWord();
    int getScore();
    int getMaxScore();
    float getAccuracy();
    int getFrequency();
    void setScore(int score);
    void setMaxScore(int maxScore);
    void setAccuracy(float accuracy);
    void setFrequency(int frequency);




};


#endif //CPP_WORD_H
