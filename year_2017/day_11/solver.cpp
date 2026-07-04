#include <cstdint>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <sys/types.h>
#include <utility>
#include <vector>
#include <unordered_map>

namespace HexGrid
{
    enum Direction : uint8_t
    {
        NORTH = 0,
        NORTH_EAST = 1,
        SOUTH_EAST = 2,
        SOUTH = 3,
        SOUTH_WEST = 4,
        NORTH_WEST = 5
    };

    class UnitVector : public std::pair<const int8_t, const int8_t>
    {
    public:
        UnitVector(const Direction d) : std::pair<const int8_t, const int8_t>(vecs[d]) {}
    private:
        inline static const std::pair<const int8_t, const int8_t> vecs[6] = { {0, -1}, {1, -1}, {1, 0}, {0, 1}, {-1, 1}, {-1, 0} };
    };

    struct Position
    {
        int q, r;

        Position& operator+=(const Direction& rhs)
        {
            auto v = UnitVector(rhs);
            q += v.first;
            r += v.second;
            return *this;
        }

        Position operator+(const Direction& rhs)
        {
            Position p = *this;
            p += rhs;
            return p;
        }
        
        uint Distance(const Position& other)
        {
            return (abs(q - other.q) + abs(r - other.r) + abs(q + r - other.q - other.r)) / 2;
        }
    };
}


static std::vector<HexGrid::Direction> readInput(const std::string& path)
{
    std::vector<HexGrid::Direction> moves;

    const std::unordered_map<std::string, HexGrid::Direction> dirMap = {
        {"n", HexGrid::Direction::NORTH},
        {"ne", HexGrid::Direction::NORTH_EAST},
        {"se", HexGrid::Direction::SOUTH_EAST},
        {"s", HexGrid::Direction::SOUTH},
        {"sw", HexGrid::Direction::SOUTH_WEST},
        {"nw", HexGrid::Direction::NORTH_WEST},
    };
    std::ifstream in(path);
    std::string line;
    if(in >> line)
    {
        std::stringstream ss(line);
        std::string token;
        while (getline(ss, token, ','))
            moves.push_back(dirMap.at(token));
    }
    return moves;
}

static uint partOne(const std::vector<HexGrid::Direction>& moves)
{
    HexGrid::Position position = {0, 0};
    for (auto move : moves)
        position += move;
    return position.Distance({0, 0});
}

static uint partTwo(const std::vector<HexGrid::Direction>& moves)
{
    uint furthest = 0;
    HexGrid::Position position = {0, 0};
    for (auto move : moves)
    {
        position += move;
        furthest = std::max(furthest, position.Distance({0, 0}));
    }
    return furthest;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<HexGrid::Direction> moves = readInput("input.txt");
    int result = (part == 1) ? partOne(moves) : partTwo(moves);
    std::cout << result << '\n';
    return 0;
}
