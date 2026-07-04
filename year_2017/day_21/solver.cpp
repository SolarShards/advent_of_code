#include <array>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <iterator>
#include <sstream>
#include <string>
#include <sys/types.h>
#include <utility>
#include <vector>
#include <bitset>
#include <unordered_map>

template<size_t size>
using Rulebook = std::unordered_map<std::bitset<size*size>, std::bitset<(size + 1)*(size + 1)>>;

template<size_t size>
void addRule(Rulebook<size>& rulebook, std::string& inPattern, std::string& outPattern)
{
    const size_t inSize = size*size;
    const size_t outSize = (size + 1)*(size + 1);

    if ((inPattern.size() != inSize) || (outPattern.size() != outSize))
        return;

    std::bitset<inSize> ip;
    for (uint8_t i = 0; i < inSize; i++)
        ip[i] = (inPattern[i] == '#');
    std::bitset<outSize> op;
    for (uint8_t i = 0; i < outSize; i++)
        op[i] = (outPattern[i] == '#');

    rulebook.insert({ip, op});
}

static const std::array<uint, 4> rotateTwo = {2, 0, 3, 1};
static const std::array<uint, 9> rotateThree = {6, 3, 0, 7, 4, 1, 8, 5, 2};

template<size_t size>
void rotate(std::bitset<size*size>& pattern)
{
    std::bitset<size*size> ret;
    for (uint i = 0; i < ret.size(); i++)
        ret[i] = pattern[(size == 2) ? rotateTwo[i] : rotateThree[i]];
    pattern = ret;
}

static const std::array<uint, 4> flipTwo = {2, 3, 0, 1};
static const std::array<uint, 9> flipThree = {6, 7, 8, 3, 4, 5, 0, 1, 2};

template<size_t size>
void flip(std::bitset<size*size>& pattern)
{
    std::bitset<size*size> ret;
    for (uint i = 0; i < ret.size(); i++)
        ret[i] = pattern[(size == 2) ? flipTwo[i] : flipThree[i]];
    pattern = ret;
}

template<size_t size>
void completeRuleBook(Rulebook<size>& rulebook)
{
    Rulebook<size> extendedRules;
    std::bitset<size*size> pattern;
    for (auto& [in, out] : rulebook)
    {
        if ((in == 0) || (in == -1))
        {
            extendedRules.insert({in, out});
            continue;
        }

        pattern = in;

        for (uint i = 0; i < 2; i++)
        {
            for (uint j = 0; j < 4; j++)
            {
                extendedRules.insert({pattern, out});
                rotate<size>(pattern);
            }
            flip<size>(pattern);
        }
    }
    rulebook = extendedRules;
}

template<size_t size>
static std::vector<std::bitset<size*size>> serialize(std::vector<std::vector<bool>>& image)
{
    std::vector<std::bitset<size*size>> ret;
    for (uint row = 0; row < image.size(); row += size)
    {
        for (uint col = 0; col < image.size(); col += size)
        {
            std::bitset<size*size> block;
            for (uint i = 0; i < size; i++)
            {
                for (uint j = 0; j < size; j++)
                {
                    block[(i * size) + j] = image[row + i][col + j];
                }
            }
            ret.push_back(block);
        }
    }
    return ret;
}

template<size_t size>
static std::vector<std::vector<bool>> deserialize(std::vector<std::bitset<size*size>>& blocks)
{
    const uint side = std::sqrt(blocks.size());
    std::vector<std::vector<bool>> ret;

    for (uint row = 0; row < side; row++)
    {
        std::array<std::vector<bool>, size> blockLine{};
        for (uint col = 0; col < side; col++)
        {
            std::bitset<size*size>& block = blocks[(row * side) + col];

            for (uint i = 0; i < size; i++)
            {
                for (uint j = 0; j < size; j++)
                {
                    blockLine[i].push_back(block[(i * size) + j]);
                }
            }
        }
        std::move(blockLine.begin(), blockLine.end(), std::back_inserter(ret));
    }
    return ret;
}

// Thought of a multithreaded version but part 2 showed it far from needed
void upscale(std::vector<std::vector<bool>>& image, const std::pair<Rulebook<2>, Rulebook<3>>& rules, uint passes)
{
    for (uint i = 0; i < passes; i++)
    {
        if ((image.size() % 2) == 0)
        {
            auto serialized = serialize<2>(image);
            std::vector<std::bitset<3*3>> upscaled;
            for (auto block : serialized)
                upscaled.push_back(rules.first.at(block));
            image = deserialize<3>(upscaled);
        }
        else 
        {
            auto serialized = serialize<3>(image);
            std::vector<std::bitset<4*4>> upscaled;
            for (auto block : serialized)
                upscaled.push_back(rules.second.at(block));
            image = deserialize<4>(upscaled);
        }
    }
}

static std::pair<Rulebook<2>, Rulebook<3>> readInput(const std::string& path)
{
    Rulebook<2> rulesOfTwo;
    Rulebook<3> rulesOfThree;
    std::ifstream in(path);
    std::vector<std::string> lines;
    std::string line, inPattern, arrow, outPattern;
    while (getline(in, line))
    {
        std::erase(line, '/');
        std::stringstream ss(line);
        ss >> inPattern >> arrow >> outPattern;
        if (inPattern.size() == 4)
            addRule<2>(rulesOfTwo, inPattern, outPattern);
        else if (inPattern.size() == 9)
            addRule<3>(rulesOfThree, inPattern, outPattern); 
    }
    completeRuleBook<2>(rulesOfTwo);
    completeRuleBook<3>(rulesOfThree);
    return std::make_pair(rulesOfTwo, rulesOfThree);
}

static uint partOne(const std::pair<Rulebook<2>, Rulebook<3>>& rules)
{
    std::vector<std::vector<bool>> image = {{0,1,0}, {0,0,1}, {1,1,1}};
    uint count = 0;
    upscale(image, rules, 5);
    for (auto line: image)
        count += std::count(line.begin(), line.end(), 1);
    return count;
}

static uint partTwo(const std::pair<Rulebook<2>, Rulebook<3>>& rules)
{
    std::vector<std::vector<bool>> image = {{0,1,0}, {0,0,1}, {1,1,1}};
    uint count = 0;
    upscale(image, rules, 18);
    for (auto line: image)
        count += std::count(line.begin(), line.end(), 1);
    return count;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::pair<Rulebook<2>, Rulebook<3>> rules = readInput("input.txt");
    uint result = (part == 1) ? partOne(rules) : partTwo(rules);
    std::cout << result << '\n';
    return 0;
}
