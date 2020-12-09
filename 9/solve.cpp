#include <vector>
#include <iterator>
#include <istream>
#include <fstream>
#include <iostream>
#include <utility>
#include <algorithm>
#include <numeric>

template <typename T> auto pairs(typename std::vector<T>::const_iterator begin, typename std::vector<T>::const_iterator end)
{
    std::vector<std::pair<T, T>> v;
    for (auto x = begin; x < end; ++x) for (auto y = begin; y < end; ++y) if (*x != *y) v.emplace_back(*x, *y);
    return v;
}

template <typename T> bool valid(typename std::vector<T>::const_iterator begin, typename std::vector<T>::const_iterator end)
{
    auto pair = pairs<T>(begin, end);

    std::vector<T> sums(pair.size());
    std::transform(pair.begin(), pair.end(), sums.begin(), [](auto x) { return x.first + x.second; });
    
    return std::find(sums.begin(), sums.end(), *end) != std::end(sums);
}

template <int N, typename T> T p1(const std::vector<T> &input)
{
    for (auto x = N; x < input.size(); ++x) if (!valid<T>(input.begin() - N + x, input.begin() + x)) return input[x];
    return 0;
}

template <typename T> auto find_range(typename std::vector<T>::const_iterator begin, typename std::vector<T>::const_iterator end, T sum)
{
    for (auto itx = begin; itx < end; ++itx) for (auto ity = itx; ity < end; ++ity) if (sum == std::accumulate(itx, ity, 0)) return std::vector<T>(itx, ity);
    return std::vector<T>();
}

template <typename T> auto p2(typename std::vector<T>::const_iterator begin, typename std::vector<T>::const_iterator end, T a)
{
    auto range = find_range<T>(begin, end, a);
    return *std::min_element(range.begin(), range.end()) + *std::max_element(range.begin(), range.end());
};

int main()
{
    auto ifstream = std::ifstream("input.txt");
    std::vector<int> input((std::istream_iterator<int>(ifstream)), std::istream_iterator<int>());
    
    auto a = p1<25>(input);
    auto b = p2<int>(input.begin(), input.end(), a);

    std::cout << a << "\n"
              << b << "\n";
}