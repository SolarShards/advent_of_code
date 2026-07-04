#include <cstdint>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>

static uint readInput(const std::string& path)
{
    uint rotation;
    std::ifstream in(path);
    in >> rotation;
    return rotation;
}

static uint partOne(const uint rotation)
{
    std::vector<uint> buffer = {0};
    uint pos = 0;
    for (uint i = 1; i <= 2017; i++)
    {
        pos = (pos + rotation) % buffer.size();
        buffer.insert(buffer.begin() + pos + 1, i);
        pos++;
    }
    return buffer[(pos + 1) % buffer.size()];
}

static uint partTwo(const uint rotation)
{
    uint64_t pos = 0;
    uint64_t latestAfterZero;
    for (uint64_t i = 1; i <= 50'000'000; i++)
    {
        pos = (pos + rotation) % i;
        if (pos == 0)
            latestAfterZero = i;
        pos++;
    }
    return latestAfterZero;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    uint rotation = readInput("input.txt");
    int result = (part == 1) ? partOne(rotation) : partTwo(rotation);
    std::cout << result << '\n';
    return 0;
}
