#include <iostream>
#include <fstream>
#include <vector>

static std::vector<int> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<int> instructions;
    int i;
    while (in >> i) {
        instructions.push_back(i);
    }
    return instructions;
}

static int partOne(std::vector<int>& instructions)
{
    int steps = 0;
    int index = 0;
    int jmp;
    while (index >= 0 && index < instructions.size())
    {
        jmp = instructions[index];
        instructions[index]++;
        index += jmp;
        steps++;
    }
    return steps;
}

static int partTwo(std::vector<int>& instructions)
{
    int steps = 0;
    int index = 0;
    int jmp;
    while (index >= 0 && index < instructions.size())
    {
        jmp = instructions[index];
        instructions[index] += instructions[index] > 2 ? -1 : 1;
        index += jmp;
        steps++;
    }
    return steps;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<int> instructions = readInput("input.txt");
    int result = (part == 1) ? partOne(instructions) : partTwo(instructions);
    std::cout << result << '\n';
    return 0;
}
