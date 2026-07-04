#include <cstdint>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <functional>

static std::vector<std::function<void(std::string&)>> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<std::function<void(std::string&)>> steps;
    std::string line, token;
    getline(in, line);
    std::stringstream ss(line);
    while (getline(ss, token, ','))
    {
        switch(token[0])
        {
            case 's':
                steps.push_back(std::bind(
                    [](std::string& programs, uint8_t n) { std::rotate(programs.rbegin(), programs.rbegin() + n, programs.rend()); },
                    std::placeholders::_1,
                    std::stoi(token.substr(1))
                ));
                break;
            case 'x':
                steps.push_back(std::bind(
                    [](std::string& programs, uint8_t a, uint8_t b) { std::swap(programs[a], programs[b]); },
                    std::placeholders::_1,
                    std::stoi(token.substr(1, token.find('/') - 1)),
                    std::stoi(token.substr(token.find('/') + 1))
                ));
                break;
            case 'p':
                steps.push_back(std::bind(
                    [](std::string& programs, char a, char b) { std::swap(programs[programs.find(a)], programs[programs.find(b)]); },
                    std::placeholders::_1,
                    token[1],
                    token[3]
                ));
                break;
            default:
                break;
        }
    }
    steps.shrink_to_fit();
    return steps;
}

static const std::string startPosition = "abcdefghijklmnop";

static void dance(std::string& programs, const std::vector<std::function<void(std::string&)>>& steps)
{
    for (auto it = steps.begin(); it != steps.end(); it++)
        (*it)(programs);
}

static std::string partOne(const std::vector<std::function<void(std::string&)>>& steps)
{
    std::string programs = startPosition;
    dance(programs, steps);
    return programs;
}

static std::string partTwo(const std::vector<std::function<void(std::string&)>>& steps)
{
    std::string programs = startPosition;
    std::vector<std::string> positions;

    do {
        positions.push_back(programs);
        dance(programs, steps);
    }
    while(programs != startPosition);

    return positions[1'000'000'000 % positions.size()];
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<std::function<void(std::string&)>> steps = readInput("input.txt");
    std::string result = (part == 1) ? partOne(steps) : partTwo(steps);
    std::cout << result << '\n';
    return 0;
}
