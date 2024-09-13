#include <iostream>
#include "include/DataParser.h"
#include <chrono>





int main() {

    std::string folderPath = "C:/Users/Dor Shukrun/Desktop/Exelanteem/full data";
    auto start = std::chrono::high_resolution_clock::now();
    DataParser dp(folderPath);
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Time taken: " << std::chrono::duration_cast<std::chrono::seconds>(end - start).count() << " seconds" << std::endl;

    while (true) {
        std::string word;
        std::cout << "Enter a word: ";
        std::cin >> word;

        if (word == "exit") {
            break;
        }

        std::vector<std::string> sen = dp.getSentencesWithWord(word);
        for (const auto &s: sen) {
            std::cout << s << std::endl;
        }
    }







    return 0;
}
