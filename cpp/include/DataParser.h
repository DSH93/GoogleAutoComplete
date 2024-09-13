//
// Created by Dor Shukrun on 13/09/2024.
//

#ifndef CPP_DATAPARSER_H
#define CPP_DATAPARSER_H

#include <string>
#include <unordered_set>
#include <vector>
#include <unordered_map>

class DataParser {
public:
    DataParser(const std::string& folderPath);
    const std::unordered_set<std::string>& getUniqueWords() const;
    const std::unordered_set<std::string>& getSentences() const;
    const std::unordered_map<std::string, std::vector<std::string>>& getWordToSentence() const;
    std::vector<std::string> getSentencesWithWord(const std::string& word) const;
    std::vector<std::string> getWordsByMinHash(int num_hashes);

private:
    std::unordered_set<std::string> uniqueWords;
    std::unordered_set<std::string> sentences;
    std::unordered_map<std::string, std::vector<std::string>> wordToSentence;



    void loadFilesFromFolder(const std::string& folderPath);
    void loadFile(const std::string& filePath);
    void processSentences();
    static void cleanSentence(std::string& sentence);
    static bool isInvalidWord(const std::string& word);
    void addSentenceToWord();
    static size_t compute_minhash(const std::string& word, int num_hashes);
    std::vector<std::string> sort_words_by_minhash(const std::unordered_set<std::string>& words, int num_hashes);
};



#endif //CPP_DATAPARSER_H
