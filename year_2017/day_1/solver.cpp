#include <cstddef>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

static std::vector<uint8_t> readInput(const std::string& path)
{
    std::vector<uint8_t> digits;
    std::ifstream file(path);
    std::string in;
    std::getline(file, in);
    digits.reserve(in.size());
    for (char c: in)
        digits.push_back(c - '0');
    return digits;
}

static uint32_t partOne(const std::vector<uint8_t>& digits)
{
    uint32_t result = 0;
    for (size_t i = 0; i < digits.size(); i++)
    {
        if (digits[i] == digits[(i+1) % digits.size()])
            result += digits[i];
    }
    return result;
}

static uint32_t partTwo(const std::vector<uint8_t>& digits)
{
    uint32_t result = 0;
    for (size_t i = 0; i < digits.size(); i++)
    {
        if (digits[i] == digits[(i + digits.size()/2) % digits.size()])
            result += digits[i];
    }
    return result;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<uint8_t> digits = readInput("input.txt");
    uint32_t result = (part == 1) ? partOne(digits) : partTwo(digits);
    std::cout << result << '\n';
    return 0;
}
