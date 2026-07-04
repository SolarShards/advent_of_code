#include <iostream>
#include <fstream>
#include <cmath>
#include <unordered_map>

static int readInput(const std::string& path)
{
    int input;
    std::ifstream file(path);
    file >> input;
    return input;
}

static int partOne(const int square)
{
    double root = sqrt(square);
    double root_floor = floor(root);
    int low_root = static_cast<int>(root_floor);

    if (!(low_root % 2))
        low_root--;
    else if (root_floor == root)
        return low_root - 1;

    int diameter = (low_root+1) / 2;
    int east_pole = low_root * low_root + diameter;

    int section = abs(square - east_pole);
    for (int i = 1; i <= 3; i++)
    {
        int p = east_pole + 2 * diameter * i;
        int s = abs(square - p);
        section = std::min(section, s);
    }

    return diameter + section;
}

inline std::pair<int, int> operator+(const std::pair<int, int>& lhs, const std::pair<int, int>& rhs)
{
    return {lhs.first + rhs.first, lhs.second + rhs.second};
}

inline std::pair<int, int>& operator+=(std::pair<int, int>& lhs, const std::pair<int, int>& rhs)
{
    lhs = lhs + rhs;
    return lhs;
}

struct PairHasher {
    size_t operator()(const std::pair<int, int>& p) const
    {
        // Combine hashes of x and y using the bitwise XOR
        return std::hash<int>()(p.first) ^ (std::hash<int>()(p.second) << 1);
    }
};

static int partTwo(const int square)
{
    constexpr int MAX_DIRECTIONS = 8;
    const std::pair<int,int> surroundings[MAX_DIRECTIONS] = {{0,-1}, {1,-1}, {1,0}, {1, 1}, {0,1}, {-1, 1}, {-1,0}, {-1,-1}};

    std::unordered_map<std::pair<int,int>,int, PairHasher> memory = {{{0,0},1}};
    std::pair<int,int> position = {0,0};
    int front = 0;
    int left = 2;
    int value;
    
    while (true)
    {
        if (!memory.count(position + surroundings[left]))
        {
            front = left;
            left = (left + 2) % MAX_DIRECTIONS;
        }

        position += surroundings[front];
        value = 0;

        for (int i = 0; i < MAX_DIRECTIONS; i++)
        {
            auto it = memory.find(position + surroundings[i]);
            if (it != memory.end())
                value += it->second;
        }

        if (value > square)
            return value;

        memory.insert({position, value});
    }
    
    return 0;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    int input = readInput("input.txt");
    int result = (part == 1) ? partOne(input) : partTwo(input);
    std::cout << result << '\n';
    return 0;
}
