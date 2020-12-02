#include <iostream>
#include <fstream>
#include <iterator>
#include <vector>
#include <string>
#include <algorithm>

struct Entry
{
    int a, b; char c; std::string str;

    friend std::istream &operator>>(std::istream &istream, Entry &entry) {
       return ((((istream >> entry.a).ignore(1) >> entry.b).ignore(1) >> entry.c).ignore(2)) >> entry.str;  
    }
};

int main() {
    auto ifstream = std::ifstream("input.txt");
    std::vector<Entry> entries((std::istream_iterator<Entry>(ifstream)), std::istream_iterator<Entry>());

    std::cout << std::count_if(entries.begin(), entries.end(), [](const auto &e) { auto count = std::count(e.str.begin(), e.str.end(), e.c); return e.a <= count && count <= e.b; }) << "\n";
    std::cout << std::count_if(entries.begin(), entries.end(), [](const auto &e) { return e.str[e.a-1] == e.c ^ e.str[e.b-1] == e.c; }) << "\n";
}