#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

static std::vector<std::vector<uint32_t>> readInput(const std::string& path)
{
    std::vector<std::vector<uint32_t>> spreadsheet;
    std::ifstream file(path);
    std::string line;
    uint32_t i;
    while (getline(file, line)) {
        std::vector<uint32_t> row;
        std::stringstream ss(line);
        while (ss >> i)
            row.push_back(i);
        spreadsheet.push_back(row);
    }
    return spreadsheet;
}

static uint32_t partOne(const std::vector<std::vector<uint32_t>>& spreadsheet)
{
    uint32_t result = 0;
    for (auto row: spreadsheet)
    {
        result += (*std::max_element(row.begin(), row.end()) - *std::min_element(row.begin(), row.end()));
    }
    return result;
}

static uint32_t partTwo(const std::vector<std::vector<uint32_t>>& spreadsheet)
{
    uint32_t result = 0;
    for (auto row: spreadsheet)
    {
        std::sort(row.begin(), row.end(), std::greater<uint32_t>());
        for (size_t i = 0; i < row.size() - 1; i++)
        {
            for (size_t j = i+1; j < row.size(); j++)
            {
                if (!(row[i] % row[j]))
                {
                    result += row[i] / row[j];
                    i = row.size();
                    break;
                }
            }
        }
    }
    return result;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<std::vector<uint32_t>> input = readInput("input.txt");
    uint32_t result = (part == 1) ? partOne(input) : partTwo(input);
    std::cout << result << '\n';
    return 0;
}
