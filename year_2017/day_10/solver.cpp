#include "KnotHash.h"

#include <iomanip>
#include <iostream>
#include <fstream>
#include <sstream>

static std::string readInput(const std::string& path)
{
    std::ifstream in(path);
    std::string input;
    in >> input;
    return input;
}

static std::string partOne(const std::string& input)
{
    std::array<uint8_t, 256> sequence;
    std::iota(sequence.begin(), sequence.end(), 0);

    std::vector<uint8_t> data;
    std::stringstream ss(input);
    std::string token;
    ulong l;
    while (getline(ss, token, ','))
    {
        if ((l = std::stoul(token)) <= UINT8_MAX)
            data.push_back(l);
    }

    std::KnotHash hasher;
    hasher.SingleRound(sequence, data);
    return std::to_string(sequence[0] * sequence[1]);
}

static std::string partTwo(const std::string& input)
{
    std::stringstream ss;
    std::KnotHash hashFunction;
    std::array<uint8_t, 16> hash = hashFunction(input);
    for (uint8_t byte : hash)
        ss << std::setfill('0') << std::setw(sizeof(uint8_t)*2) << std::hex << (uint)byte;
    return std::string(ss.str());
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::string input = readInput("input.txt");
    std::string result = (part == 1) ? partOne(input) : partTwo(input);
    std::cout << result << '\n';
    return 0;
}
