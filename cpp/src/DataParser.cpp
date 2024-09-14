//
// Created by Dor Shukrun on 13/09/2024.
//

#include "../include/DataParser.h"
#include <filesystem>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <cctype>
#include <iostream>

namespace fs = std::filesystem;

// Constructor: Initializes by loading files and processing sentences
DataParser::DataParser(const std::string& folderPath) {
    loadFilesFromFolder(folderPath);
    processSentences();
}

// File reading functions
void DataParser::loadFilesFromFolder(const std::string& folderPath) {
    std::cout << "Processing files..." << std::endl;
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

// Sentence processing
void DataParser::processSentences() {
    addSentenceToWord();
    sortWords();
    std::cout << "Finished processing files" << std::endl;
}

void DataParser::addSentenceToWord() {
    int size = 0;
    for (auto sentence : sentences) {
        cleanSentence(const_cast<std::string &>(sentence));
        std::istringstream iss(sentence);
        std::string word;
        while (iss >> word) {
            if (!isInvalidWord(word)) {
                size = word.size();
                auto& temp = wordsCountAndLength[size];
                for (int i = 0; i < temp.size(); ++i) {
                    temp[i].try_emplace(word, 1).first->second++;
                }
                wordToSentence[word].push_back(sentence);
            }
        }
    }
}

// Word processing and cleaning
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

bool DataParser::isInvalidWord(const std::string& word) {
    if (word.length() > 20) {
        return true;
    }
    return std::any_of(word.begin(), word.end(), [](char c) {
        return !std::isalpha(c);
    });
}

// Sorting words by MinHash
void DataParser::sortWords() {
    for (int i = 0; i < wordsCountAndLength.size(); ++i) {
        auto& temp = wordsCountAndLength[i];
        for (int j = 0; j < temp.size(); ++j) {
            std::vector<std::pair<std::string, int>> words;
            for (const auto& word : temp[j]) {
                words.emplace_back(word.first, word.second);
            }
            sort_words_by_minhash(words, 30);
        }
    }
}

void DataParser::sort_words_by_minhash(std::vector<std::pair<std::string, int>>& words, int num_hashes) {
    // Create a vector to store the words and their corresponding MinHash values.
    std::vector<std::pair<std::string, size_t>> word_minhash_pairs;

    // Calculate MinHash for each word and store it in a separate vector.
    for (const auto& word_pair : words) {
        size_t minhash = compute_minhash(word_pair.first, num_hashes);
        word_minhash_pairs.emplace_back(word_pair.first, minhash);  // Store word and MinHash
    }

    // Sort the `word_minhash_pairs` based on the MinHash values.
    std::sort(word_minhash_pairs.begin(), word_minhash_pairs.end(),
              [](const auto& lhs, const auto& rhs) {
                  return lhs.second < rhs.second;  // Sort based on MinHash values
              });

    // Create a new sorted vector for `words`.
    std::vector<std::pair<std::string, int>> sorted_words;
    for (const auto& pair : word_minhash_pairs) {
        // Find the original pair in `words` and push it into `sorted_words`
        for (const auto& word_pair : words) {
            if (word_pair.first == pair.first) {
                sorted_words.push_back(word_pair);
                break;  // Once found, move to the next word
            }
        }
    }

    // Replace the original `words` vector with the sorted one.
    words = std::move(sorted_words);
}

// Utility functions
size_t DataParser::compute_minhash(const std::string& word, int num_hashes) {
    std::hash<std::string> hasher;
    size_t min_hash = std::numeric_limits<size_t>::max();
    for (int i = 0; i < num_hashes; ++i) {
        size_t hash_value = hasher(word) ^ (i * 31);  // Apply different seed
        min_hash = std::min(min_hash, hash_value);
    }
    return min_hash;
}

// Getters
const std::unordered_map<std::string, std::vector<std::string>>& DataParser::getWordToSentence() const {
    return wordToSentence;
}

const std::unordered_map<int, std::vector<std::unordered_map<std::string, int>>>& DataParser::getWordsCountAndLength() const {
    return wordsCountAndLength;
}

std::vector<std::string> DataParser::getSentencesWithWord(const std::string& word) const {
    auto it = wordToSentence.find(word);
    if (it == wordToSentence.end()) {
        return {};
    }
    return it->second;
}
