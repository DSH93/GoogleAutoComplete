//
// Created by Dor Shukrun on 13/09/2024.
//

#ifndef CPP_DATAPARSER_H
#define CPP_DATAPARSER_H

#include <string>
#include <unordered_set>
#include <vector>
#include <unordered_map>
#include "../include/Line.h"



class DataParser {
public:
    DataParser(const std::string& folderPath);
    const std::unordered_map<std::string, std::vector<std::string>>& getWordToSentence() const;
    const std::unordered_map<int, std::vector<std::pair<std::string, int>>>& getWordsCountAndLength() const;
    std::vector<std::string> getSentencesWithWord(const std::string& word) const;


private:
    std::unordered_map<int, std::vector<std::pair<std::string, int>>> wordsCountAndLength;
    std::unordered_set<Line> sentences;
    std::unordered_map<std::string, std::vector<std::string>> wordToSentence;


    void loadFilesFromFolder(const std::string& folderPath);
    void loadFile(const std::string& filePath);
    void processSentences();
    static void cleanSentence(std::string& sentence);
    static bool isInvalidWord(const std::string& word);
    void addSentenceToWord();
    void sortWords();
    static size_t compute_minhash(const std::string& word, int num_hashes);
    static void sort_words_by_minhash(std::vector<std::pair<std::string, int>>& words, int num_hashes);
};



#endif //CPP_DATAPARSER_H
