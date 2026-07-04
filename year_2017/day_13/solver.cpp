#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <regex>

static std::unordered_map<uint, uint> readInput(const std::string& path)
{
    std::unordered_map<uint, uint> layers;

    std::ifstream in(path);
    std::string line;
    std::regex re("(\\d+): (\\d+)");
    std::smatch match;

    while (getline(in, line)) 
    {
        if (std::regex_search(line, match, re))
            layers.insert({std::stoi(match.str(1)), std::stoi(match.str(2))});
    }
    return layers;
}

bool scannerPresent(const uint depth, const uint range, const uint delay = 0)
{
    return ((depth + delay) % ((range - 1) * 2)) == 0;
}

static uint partOne(const std::unordered_map<uint, uint>& layers)
{
    uint severity = 0;
    for (auto layer : layers)
    {
        if (scannerPresent(layer.first, layer.second))
            severity += layer.first * layer.second;
    }
    return severity;
}

static uint partTwo(const std::unordered_map<uint, uint>& layers)
{
    uint delay = 0;
    bool detected = true;
    while (detected)
    {
        detected = false;
        delay++;
        for (auto layer : layers)
        {
            if (scannerPresent(layer.first, layer.second, delay))
            {
                detected = true;
                break;
            }
        }
    }
    return delay;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::unordered_map<uint, uint> layers = readInput("input.txt");
    uint result = (part == 1) ? partOne(layers) : partTwo(layers);
    std::cout << result << '\n';
    return 0;
}
