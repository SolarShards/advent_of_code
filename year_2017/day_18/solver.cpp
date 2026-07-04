#include "ThreadSafeQueue.h"

#include <cctype>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <thread>
#include <vector>
#include <list>
#include <array>
#include <tuple>
#include <functional>
#include <unordered_map>


class Computer
{
public:
    Computer(): _instructionSet(baseInstructionSet)
    {
        for(char c = 'a'; c <= 'z'; c++)
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

            if (opcode == "snd" || opcode == "rcv")
                y = nullptr;
            else if (std::islower(rhs[0]))
                y = &_registers.at(rhs[0]);
            else
            {
                _rodata.push_back(std::stoi(rhs));
                y = &_rodata.back();
            }

            _program.push_back(std::make_tuple(_instructionSet.at(opcode), x, y));
        }
    }

    int64_t GetFirstRecoveredFrequency()
    {
        for (auto& reg : _registers)
            reg.second = 0;
        _pc = 0;
        _playingFrequency = INT64_MIN;
        _recoveredFrequency = INT64_MIN;

        while (_pc >= 0 && _pc < _program.size())
        {
            auto [op, x, y] = _program[_pc];
            op(*this, x, y);
            if (_recoveredFrequency != INT64_MIN)
                break;
        }
        return _recoveredFrequency;
    }

protected:
    void snd(int64_t* x, int64_t* y)
    {
        (void)y;
        _pc++;
        _playingFrequency = *x;
    }

    void rcv(int64_t* x, int64_t* y)
    {
        (void)y;
        _pc++;
        if (*x != 0)
            _recoveredFrequency = _playingFrequency;
    }

    void jgz(int64_t* x, int64_t* y)
    {
        _pc += (*x > 0) ? *y : 1;
    }

    void set(int64_t* x, int64_t* y)
    {
        _pc++;
        *x = *y;
    }

    void add(int64_t* x, int64_t* y)
    {
        _pc++;
        *x += *y;
    }

    void mul(int64_t* x, int64_t* y)
    {
        _pc++;
        *x *= *y;
    }

    void mod(int64_t* x, int64_t* y)
    {
        _pc++;
        *x %= *y;
    }

    static inline const std::unordered_map<std::string, std::function<void(Computer&, int64_t*, int64_t*)>> baseInstructionSet = {
        {"snd", &Computer::snd},
        {"rcv", &Computer::rcv},
        {"jgz", &Computer::jgz},
        {"set", &Computer::set},
        {"add", &Computer::add},
        {"mul", &Computer::mul},
        {"mod", &Computer::mod}
    };

    std::unordered_map<std::string, std::function<void(Computer&, int64_t*, int64_t*)>> _instructionSet;
    std::unordered_map<char, int64_t> _registers;
    std::list<int64_t> _rodata;
    std::vector<std::tuple<std::function<void(Computer&, int64_t*, int64_t*)>, int64_t*, int64_t*>> _program;
    int64_t _pc;
    int64_t _playingFrequency;
    int64_t _recoveredFrequency;
};

class DuetComputer: public Computer
{
public:
    DuetComputer(int64_t id): _id(id), _pairedDevice(nullptr)
    {
        _instructionSet.at("snd") = [](Computer& c, int64_t* x, int64_t* y) { static_cast<DuetComputer&>(c).snd(x, y); };
        _instructionSet.at("rcv") = [](Computer& c, int64_t* x, int64_t* y) { static_cast<DuetComputer&>(c).rcv(x, y); };
    }

    ~DuetComputer()
    {
        DetachPairedDevice();
    }

    ThreadSafeQueue<int64_t>& GetRcvQueue() { return _rcvQueue; }
    uint64_t GetSndCounter() { return _sndCounter; }
    bool IsWaiting() { return _isReceiving && _rcvQueue.empty(); }

    void PairDevice(DuetComputer& other)
    {
        if (_pairedDevice == nullptr)
        {
            _pairedDevice = &other;
            other.PairDevice(*this);
        }
    }

    void DetachPairedDevice()
    {
        if (_pairedDevice != nullptr)
        {
            DuetComputer* p = nullptr;
            std::swap(p, _pairedDevice);
            p->DetachPairedDevice();
        }
    }

    void Run()
    {
        for (auto& reg : _registers)
            reg.second = 0;
        _pc = 0;
        _registers.at('p') = _id;
        _sndCounter = 0;
        _killSignal = false;
        _rcvQueue.clear();

        while ((_pc >= 0) && (_pc < _program.size()) && !_killSignal)
        {
            auto [op, x, y] = _program[_pc];
            op(*this, x, y);
        }
    }

private:
    int64_t GetFirstRecoveredFrequency() = delete;

    void snd(int64_t* x, int64_t* y)
    {
        (void)y;
        _pc++;
        _sndCounter++;
        if (_pairedDevice != nullptr)
            _pairedDevice->GetRcvQueue().ThreadSafePush(*x);
    }

    void rcv(int64_t* x, int64_t* y)
    {
        (void)y;

        _pc++;
        _isReceiving = true;

        if (IsWaiting() && _pairedDevice->IsWaiting())
        {
            _pairedDevice->Terminate();
            _pairedDevice->GetRcvQueue().ThreadSafePush(0);
            _killSignal = true;
            return;
        }

        *x = _rcvQueue.ThreadSafePop();
        _isReceiving = false;
    }

    void Terminate() 
    {
        _killSignal = true;
    }

    ThreadSafeQueue<int64_t> _rcvQueue;
    DuetComputer* _pairedDevice;
    int64_t _id;
    uint64_t _sndCounter;
    bool _isReceiving;
    bool _killSignal;
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
    return c.GetFirstRecoveredFrequency();
}

static int64_t partTwo(std::vector<std::array<std::string, 3>>& assembly)
{
    DuetComputer c0(0), c1(1);
    c0.LoadProgram(assembly);
    c1.LoadProgram(assembly);
    c0.PairDevice(c1);
    std::thread t1(&DuetComputer::Run, &c1);
    std::thread t0(&DuetComputer::Run, &c0);
    t0.join();
    t1.join();
    return c1.GetSndCounter();
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<std::array<std::string, 3>> assembly = readInput("input.txt");
    int64_t result = (part == 1) ? partOne(assembly) : partTwo(assembly);
    std::cout << result << '\n';
    return 0;
}
