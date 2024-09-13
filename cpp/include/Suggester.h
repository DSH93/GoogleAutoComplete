//
// Created by Dor Shukrun on 13/09/2024.
//

#ifndef CPP_SUGGESTER_H
#define CPP_SUGGESTER_H


#include <iostream>
#include "DataParser.h"
#include <string>

class Suggester {
private:
    std::vector<std::string> uniqueWords;
    std::unordered_map<std::string, std::vector<std::string>> wordToSentence;
    std::string path;

public:
    Suggester(std::string path);
    ~Suggester();
    void suggest();

};


#endif //CPP_SUGGESTER_H
