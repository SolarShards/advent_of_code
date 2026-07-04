#include <iostream>
#include <fstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <regex>

static std::unordered_map<uint, std::unordered_set<uint>> readInput(const std::string& path)
{
    std::unordered_map<uint, std::unordered_set<uint>> pipes;
    std::ifstream in(path);
    std::string line;
    std::regex re("(\\d+)");
    std::smatch match;
    uint index;

    while (getline(in, line)) 
    {
        if (!std::regex_search(line, match, re))
            continue;

        index = std::stoi(match.str(0));
        pipes.insert({index, std::unordered_set<uint>()});
        line = match.suffix().str();

        while (std::regex_search(line, match, re))
        {
            pipes[index].insert(std::stoi(match.str(0)));
            line = match.suffix().str();
        }
    }
    return pipes;
}

static std::unordered_set<uint> findGroup(const std::unordered_map<uint, std::unordered_set<uint>>& pipes, uint program)
{
    std::unordered_set<uint> group = {program};
    std::unordered_set<uint> connected = pipes.at(program);

    while (!connected.empty())
    {
        std::unordered_set<uint> toAdd;
        for (uint p : connected)
            toAdd.insert(pipes.at(p).begin(), pipes.at(p).end());

        group.insert(connected.begin(), connected.end());

        connected.clear();
        for (uint p : toAdd)
        {
            if (!group.count(p))
                connected.insert(p);
        }
    }
    return group;
}

static uint partOne(const std::unordered_map<uint, std::unordered_set<uint>>& pipes)
{
    return findGroup(pipes, 0).size();
}

static uint partTwo(const std::unordered_map<uint, std::unordered_set<uint>>& pipes)
{
    uint count = 0;
    std::unordered_set<uint> programs;
    for (auto it = pipes.begin(); it != pipes.end(); it++)
    {
        if (programs.count(it->first))
            continue;
        auto group = findGroup(pipes, it->first);
        programs.insert(group.begin(), group.end());
        count++;
    }
    return count;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    auto pipes = readInput("input.txt");
    uint result = (part == 1) ? partOne(pipes) : partTwo(pipes);
    std::cout << result << '\n';
    return 0;
}
