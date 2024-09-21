#include "include/DataParser.h"
#include "include/Suggester.h"





int main(int argc, char** argv) {
    std::string folderPath = "C:\\Users\\Dor Shukrun\\Desktop\\Exelanteem\\mvp data";

    while (true) {
        Suggester suggester(folderPath);
        suggester.suggest();
    }







    return 0;
}
