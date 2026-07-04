#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <list>
#include <unordered_map>
#include <functional>


class Computer
{
public:
    Computer(): _instructionSet(baseInstructionSet)
    {
        for(char c = 'a'; c <= 'h'; c++)
            _registers.insert({c, 0});
    }

    void LoadProgram(std::vector<std::array<std::string, 3>> assembly)
    {
        std::function<void(Computer&, int64_t*, int64_t*)> op;
        int64_t *x, *y;

        _program.clear();
        _rodata.clear();

        for (auto& [opcode, lhs, rhs] : assembly)
        {
            if (std::islower(lhs[0]))
                x = &_registers.at(lhs[0]);
            else
            {
                _rodata.push_back(std::stoi(lhs));
                x = &_rodata.back();
            }

            if (std::islower(rhs[0]))
                y = &_registers.at(rhs[0]);
            else
            {
                _rodata.push_back(std::stoi(rhs));
                y = &_rodata.back();
            }

            _program.push_back(std::make_tuple(_instructionSet.at(opcode), x, y));
        }
    }

    uint Debug()
    {
        uint mulCalls = 0;
        for (auto& reg : _registers)
            reg.second = 0;
        _pc = 0;

        while (_pc >= 0 && _pc < _program.size())
        {
            auto [op, x, y] = _program[_pc];
            op(*this, x, y);
            if (*op.target<void (Computer::*)(int64_t *, int64_t *)>() == &Computer::mul)
                mulCalls++;
        }
        return mulCalls;
    }

    /* I saw the pattern of for loops but did not find the optimization good enough
    to do like I did in year 2016 day 23, therefore I'll run the beginning of the
    machine code to initialize registers, then I'll run the procedure as decompiled C++. */
    uint RunOptimized()
    {
        for (auto& reg : _registers)
            reg.second = 0;
        _pc = 0;

        _registers['a'] = 1;

        while (_pc >= 0 && _pc < 8)
        {
            auto [op, x, y] = _program[_pc];
            op(*this, x, y);
        }

        int64_t start = _registers['b'];
        int64_t end = _registers['c'];
        int64_t increment = -(*std::get<2>(*(_program.end()-2)));

        for (int64_t i = start; i <= end; i += increment)
        {
            for (int64_t j = 2; j < i; j++)
            {
                if ((i % j) == 0)
                {
                    _registers['h']++;
                    break;
                }
            }
        }

        return _registers['h'];
    }

protected:
    void set(int64_t* x, int64_t* y)
    {
        _pc++;
        *x = *y;
    }

    void sub(int64_t* x, int64_t* y)
    {
        _pc++;
        *x -= *y;
    }

    void mul(int64_t* x, int64_t* y)
    {
        _pc++;
        *x *= *y;
    }

    void jnz(int64_t* x, int64_t* y)
    {
        _pc += (*x != 0) ? *y : 1;
    }

    static inline const std::unordered_map<std::string, std::function<void(Computer&, int64_t*, int64_t*)>> baseInstructionSet = {
        {"set", &Computer::set},
        {"sub", &Computer::sub},
        {"mul", &Computer::mul},
        {"jnz", &Computer::jnz}
    };

    std::unordered_map<std::string, std::function<void(Computer&, int64_t*, int64_t*)>> _instructionSet;
    std::unordered_map<char, int64_t> _registers;
    std::list<int64_t> _rodata;
    std::vector<std::tuple<std::function<void(Computer&, int64_t*, int64_t*)>, int64_t*, int64_t*>> _program;
    int64_t _pc;
};

static std::vector<std::array<std::string, 3>> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<std::array<std::string, 3>> assembly;
    std::string line;
    while (getline(in, line))
    {
        std::stringstream ss(line);
        std::array<std::string, 3> instruction;
        ss >> instruction[0] >> instruction[1] >> instruction[2];
        assembly.push_back(instruction);
    }

    return assembly;
}

static int64_t partOne(std::vector<std::array<std::string, 3>>& assembly)
{
    Computer c;
    c.LoadProgram(assembly);
    return c.Debug();
}

static int64_t partTwo(std::vector<std::array<std::string, 3>>& assembly)
{
    Computer c;
    c.LoadProgram(assembly);
    return c.RunOptimized();
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<std::array<std::string, 3>> assembly = readInput("input.txt");
    int64_t result = (part == 1) ? partOne(assembly) : partTwo(assembly);
    std::cout << result << '\n';
    return 0;
}
