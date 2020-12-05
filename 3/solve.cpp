#include <string>
#include <vector>
#include <iterator>
#include <iostream>
#include <istream>
#include <fstream>
#include <tuple>
#include <functional>
#include <algorithm>
#include <numeric>
#include <execution>

struct Entry : public std::string
{
    bool operator[](size_t i) const {
        return this->at(i % length()) == '#';
    }
};

int main() {
    auto ifstream = std::ifstream("input.txt");
    std::vector<Entry> entries((std::istream_iterator<Entry>(ifstream)), std::istream_iterator<Entry>());
    
    auto slope = [](const std::vector<Entry> &e, std::tuple<int, int> slope) {
        auto [dx, dy] = slope;
        size_t count = 0;
        for (size_t x = 0, y = 0; y < e.size(); x += dx, y += dy) if (e[y][x]) ++count;
        return count;
    };

    std::cout << slope(entries, { 3, 1 }) << "\n";

    std::vector<std::tuple<int, int>> slopes = { {1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2} };
    auto product = std::transform_reduce(std::execution::par, slopes.begin(), slopes.end(), 1ULL, std::multiplies<size_t>(), std::bind(slope, std::ref(entries), std::placeholders::_1));
    std::cout << product << "\n";
}