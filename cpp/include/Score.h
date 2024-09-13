//
// Created by Dor Shukrun on 13/09/2024.
//

#ifndef CPP_SCORE_H
#define CPP_SCORE_H

#include <string>
#include <vector>

class WordScorer {
public:

    int calculateCustomScore(const std::string& inputWord, const std::string& word);

private:

    bool isValidSubstring(const std::string& inputWord, const std::string& candidateWord);


    int levenshteinDistance(const std::string& s1, const std::string& s2);


    struct EditOperation {
        char type; // 'replace', 'insert', 'delete'
        int index;
    };


    std::vector<EditOperation> editOperations(const std::string& s1, const std::string& s2);
};

#endif // WORDSCORER_H



