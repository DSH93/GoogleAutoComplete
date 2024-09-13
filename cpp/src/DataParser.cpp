#include "../include/DataParser.h"
#include <filesystem>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cctype>

namespace fs = std::filesystem;

DataParser::DataParser(const std::string& folderPath) {
    loadFilesFromFolder(folderPath);
    processSentences();
}

const std::unordered_set<std::string>& DataParser::getUniqueWords() const {
    return uniqueWords;
}

const std::unordered_set<std::string>& DataParser::getSentences() const {
    return sentences;
}

void DataParser::loadFilesFromFolder(const std::string& folderPath) {
    for (const auto& entry : fs::directory_iterator(folderPath)) {
        if (entry.path().extension() == ".txt") {
            loadFile(entry.path().string());
        }
    }
}

void DataParser::loadFile(const std::string& filePath) {
    std::ifstream file(filePath);
    std::string line;
    while (std::getline(file, line)) {
        if (!line.empty()) {
            sentences.insert(line);
        }
    }
    file.close();
}


void DataParser::processSentences() {
    addSentenceToWord();
}

void DataParser::cleanSentence(std::string& sentence) {

    sentence.erase(std::remove_if(sentence.begin(), sentence.end(),
                                  [](unsigned char c) { return std::iscntrl(c); }), sentence.end());


    sentence.erase(std::remove_if(sentence.begin(), sentence.end(),
                                  [](unsigned char c) { return std::ispunct(c); }), sentence.end());


    std::transform(sentence.begin(), sentence.end(), sentence.begin(),
                   [](unsigned char c) { return std::tolower(c); });


    sentence = std::string(sentence.begin(), std::unique(sentence.begin(), sentence.end(),
                                                         [](char a, char b) { return std::isspace(a) && std::isspace(b); }));
}

std::vector<std::string>  DataParser::sort_words_by_minhash(const std::unordered_set<std::string>& words, int num_hashes) {
    std::vector<std::pair<std::string, size_t>> word_minhash_pairs;

    // Calculate MinHash for each word
    for (const auto& word : words) {
        size_t minhash = compute_minhash(word, num_hashes);
        word_minhash_pairs.emplace_back(word, minhash);
    }

    // Sort words based on their MinHash values
    std::sort(word_minhash_pairs.begin(), word_minhash_pairs.end(),
              [](const auto& lhs, const auto& rhs) {
                  return lhs.second < rhs.second;
              });

    // Extract sorted words
    std::vector<std::string> sorted_words;
    for (const auto& pair : word_minhash_pairs) {
        sorted_words.push_back(pair.first);
    }

    return sorted_words;
}

size_t  DataParser::compute_minhash(const std::string& word, int num_hashes) {
    std::hash<std::string> hasher;
    size_t min_hash = std::numeric_limits<size_t>::max();
    for (int i = 0; i < num_hashes; ++i) {
        size_t hash_value = hasher(word) ^ (i * 31);  // Apply different seed
        min_hash = std::min(min_hash, hash_value);
    }
    return min_hash;
}

 bool DataParser::isInvalidWord(const std::string& word) {
    if (word.length() > 20) {
        return true;
    }

    return std::any_of(word.begin(), word.end(), [](char c)  {
        return !std::isalpha(c);
    });
}

std::vector<std::string> DataParser::getSentencesWithWord(const std::string& word) const {
    auto it = wordToSentence.find(word);
    if (it == wordToSentence.end()) {
        return {};
    }
    return it->second;
}




void DataParser::addSentenceToWord() {
    for (auto sentence : sentences){
        cleanSentence(const_cast<std::string &>(sentence));
        std::istringstream iss(sentence);
        std::string word;
        while (iss >> word) {
            if (!isInvalidWord(word)) {
                uniqueWords.insert(word);
                wordToSentence[word].push_back(sentence);
            }
        }
    }

}

std::vector<std::string> DataParser::getWordsByMinHash(int num_hashes) {
    return sort_words_by_minhash(uniqueWords, num_hashes);
}

const std::unordered_map<std::string, std::vector<std::string>>& DataParser::getWordToSentence() const {
    return wordToSentence;
}