cmake_minimum_required(VERSION 3.28)
project(cpp)

set(CMAKE_CXX_STANDARD 17)

add_executable(cpp main.cpp
        src/DataParser.cpp
        include/DataParser.h
        src/Score.cpp
        include/Score.h
        src/Suggester.cpp
        include/Suggester.h
        src/Word.cpp
        include/Word.h
)
