#include <algorithm>
#include <functional>
#include <iostream>
#include <fstream>
#include <string>
#include <sys/types.h>
#include <utility>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <regex>

class Computer
{
public:

    struct Instruction
    {
        std::string reg;
        std::function<void(int&,int&)> op;
        int val;
        std::string cmpReg;
        std::function<bool(int&,int&)> cmp;
        int cmpVal;
    };

    static inline const std::unordered_map<std::string, std::function<void(int&,int&)>> OPERATORS = {
        {"inc", [] (int& lhs, int& rhs) { lhs += rhs; }},
        {"dec", [] (int& lhs, int& rhs) { lhs -= rhs; }}
    };

    static inline const std::unordered_map<std::string, std::function<bool(int&,int&)>> COMPARATORS = {
        {"<",  [] (int& lhs, int& rhs) -> bool { return lhs < rhs; }},
        {">",  [] (int& lhs, int& rhs) -> bool { return lhs > rhs; }},
        {"<=", [] (int& lhs, int& rhs) -> bool { return lhs <= rhs; }},
        {">=", [] (int& lhs, int& rhs) -> bool { return lhs >= rhs; }},
        {"==", [] (int& lhs, int& rhs) -> bool { return lhs == rhs; }},
        {"!=", [] (int& lhs, int& rhs) -> bool { return lhs != rhs; }},
    };

    Computer(std::unordered_set<std::string>& regs, std::vector<Instruction> & prog)
    : _program(std::move(prog)) 
    {
        for (std::string r : regs)
            _registers.insert({r, 0});
    }

    int ReadLargestValue(void)
    {
        return std::max_element(
            _registers.begin(), _registers.end(), 
            [](const auto& lhs, const auto& rhs) { return lhs.second < rhs.second; }
        )->second;
    }

    int ReadAllTimeHighest(void) { return _allTimeHighest; }

    void Run()
    {
        for (Instruction i : _program)
        {
            if (i.cmp(_registers[i.cmpReg], i.cmpVal))
                i.op(_registers[i.reg], i.val);
            _allTimeHighest = std::max(_allTimeHighest, ReadLargestValue());
        }
    }

private:
    std::unordered_map<std::string, int> _registers;
    std::vector<Instruction> _program;
    int _allTimeHighest;
};

static Computer readInput(const std::string& path)
{
    std::unordered_set<std::string> registers;
    std::vector<Computer::Instruction> instructions;

    std::ifstream in(path);
    std::string line;
    std::regex re("(\\w+) (inc|dec) (\\d+|-\\d+) if (\\w+) (\\S+) (\\d+|-\\d+)");
    std::smatch match;

    while (getline(in, line))
    {
        if (!std::regex_search(line, match, re))
            continue;

        registers.insert(match.str(1));

        instructions.push_back({
            .reg = match.str(1),
            .op = Computer::OPERATORS.at(match.str(2)),
            .val = std::stoi(match.str(3)),
            .cmpReg = match.str(4),
            .cmp = Computer::COMPARATORS.at(match.str(5)),
            .cmpVal = std::stoi(match.str(6))
            
        });
    }

    return Computer(registers, instructions);
}

static int partOne(Computer& c)
{
    c.Run();
    return c.ReadLargestValue();
}

static int partTwo(Computer& c)
{
    c.Run();
    return c.ReadAllTimeHighest();
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    Computer c = readInput("input.txt");
    int result = (part == 1) ? partOne(c) : partTwo(c);
    std::cout << result << '\n';
    return 0;
}
