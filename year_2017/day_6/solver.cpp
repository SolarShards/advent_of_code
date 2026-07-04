#include <algorithm>
#include <iostream>
#include <fstream>
#include <string>
#include <array>
#include <vector>

static std::array<uint, 16> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::array<uint, 16> banks;
    uint bank;
    for (int i = 0; i < 16; i++) {
        in >> banks[i];
    }
    return banks;
}

static void balance(const std::array<uint, 16>& banks)
{
    uint* balancer = const_cast<uint*>(std::max_element(banks.begin(), banks.end()));
    uint blocks = *balancer;
    *balancer = 0;

    while(blocks)
    {
        balancer = (balancer == const_cast<uint*>(banks.end() - 1)) ? const_cast<uint*>(banks.begin()) : balancer + 1;
        blocks--;
        (*balancer)++;
    }
}

static int partOne(const std::array<uint, 16>& banks)
{
    std::vector<std::array<uint, 16>> configs = {banks};
    uint cycles = 0;

    while (true)
    {
        balance(banks);
        cycles++;
        if (std::count(configs.begin(), configs.end(), banks))
            return cycles;
        configs.push_back(banks);
    }
}

static int partTwo(const std::array<uint, 16>& banks)
{
    partOne(banks);
    std::array<uint, 16> target = banks;
    uint cycles = 0;

    while (true)
    {
        balance(banks);
        cycles++;
        if (banks == target)
            return cycles;
    }

    return cycles;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::array<uint, 16> banks = readInput("input.txt");
    int result = (part == 1) ? partOne(banks) : partTwo(banks);
    std::cout << result << '\n';
    return 0;
}
