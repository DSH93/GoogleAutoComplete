//
// Created by Dor Shukrun on 22/09/2024.
//

#ifndef CPP_LINE_H
#define CPP_LINE_H


#include <string>

#include <functional>

class Line {
public:
    std::string file;
    int line;
    std::string sen;
    bool operator==(const Line& other) const {
        return file == other.file && line == other.line && sen == other.sen;
    }
};

namespace std {
    template <>
    struct hash<Line> {
        std::size_t operator()(const Line& l) const {
            return std::hash<std::string>()(l.file) ^ std::hash<int>()(l.line) ^ std::hash<std::string>()(l.sen);
        }
    };
}


#endif //CPP_LINE_H
