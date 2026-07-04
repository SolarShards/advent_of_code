#include <cstdint>
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <regex>

class TuringMachine
{
public:
    struct State
    {
        struct Branch
        {
            bool setBit, moveRight;
            char setState;
        };
        Branch branches[2];
    };


    TuringMachine(std::unordered_map<char, State>& states, char initState, uint64_t steps)
    : _pos(0), _states(std::move(states)), _sts(&_states.at(initState)), _steps(steps) {}

    uint64_t Run()
    {
        for (uint64_t i = 0; i < _steps; i++)
        {
            State::Branch b = _sts->branches[_tape.count(_pos)];
            
            if (b.setBit)
                _tape.insert(_pos);
            else
                _tape.erase(_pos);

            _pos += b.moveRight ? 1 : -1;

            _sts = &_states.at(b.setState);
        }

        return _tape.size();
    }

private:
    std::unordered_set<int64_t> _tape;
    int64_t _pos;
    std::unordered_map<char, State> _states;
    State* _sts;
    uint64_t _steps;
};

static TuringMachine readInput(const std::string& path)
{
    std::ifstream in(path);
    std::string blueprint;
    std::stringstream ss;
    char initState;
    uint steps;
    std::unordered_map<char, TuringMachine::State> states;
    std::regex re;
    std::smatch match;

    ss << in.rdbuf();
    blueprint = ss.str();

    re.assign("Begin in state (\\w)\\.");
    if (!std::regex_search(blueprint, match, re))
        throw std::runtime_error("Could not find the initial state in the blueprint.");
    initState = match[1].str()[0];

    re.assign("Perform a diagnostic checksum after (\\d+) steps.");
    if (!std::regex_search(blueprint, match, re))
        throw std::runtime_error("Could not find the number of steps in the blueprint.");
    steps = std::stoi(match[1]);

    re.assign(
        "In state (\\w):\\n"
        "  If the current value is 0:\\n"
        "    - Write the value (\\d).\\n"
        "    - Move one slot to the (left|right).\\n"
        "    - Continue with state (\\w).\\n"
        "  If the current value is 1:\\n"
        "    - Write the value (\\d).\\n"
        "    - Move one slot to the (left|right).\\n"
        "    - Continue with state (\\w)."
    );
    while (std::regex_search(blueprint, match, re))
    {
        char c = match[1].str()[0];
        states.insert({match[1].str()[0], TuringMachine::State({
            TuringMachine::State::Branch({
                .setBit = static_cast<bool>(std::stoi(match[2])),
                .moveRight = (match[3] == "right"),
                .setState = match[4].str()[0]
            }),
            TuringMachine::State::Branch({
                .setBit = static_cast<bool>(std::stoi(match[5])),
                .moveRight = (match[6] == "right"),
                .setState = match[7].str()[0]
            })
        })});
        blueprint = match.suffix().str();
    }

    return TuringMachine(states, initState, steps);
}

static uint64_t partOne(TuringMachine& cpu)
{
    return cpu.Run();
}

int main(int argc, char** argv)
{
    TuringMachine cpu = readInput("input.txt");
    std::cout << partOne(cpu) << '\n';
    return 0;
}
