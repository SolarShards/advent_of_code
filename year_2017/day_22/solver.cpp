#include <iostream>
#include <fstream>
#include <string>
#include <unordered_set>
#include <utility>

struct Node
{
    int x, y;
    bool operator==(const Node& other) const { return (x == other.x) && (y == other.y);}
    Node& operator+=(const Node& other)
    {
        x += other.x;
        y += other.y;
        return *this;
    }
    Node operator+(const Node& other) const
    {
        Node sum = *this;
        sum += other;
        return sum;
    }
};

struct NodeHasher {
    size_t operator()(const Node& n) const
    {
        // Combine hashes of x and y using the bitwise XOR
        return std::hash<int>()(n.x) ^ (std::hash<int>()(n.y) << 1);
    }
};

static const Node unitVector[4] = {{0, -1}, {-1, 0}, {0, 1}, {1, 0}};

static std::pair<std::unordered_set<Node, NodeHasher>, Node> readInput(const std::string& path)
{
    std::unordered_set<Node, NodeHasher> grid;
    std::ifstream in(path);
    std::string row;
    int x;
    int y = 0;
    while (getline(in, row))
    {
        for (int x = 0; x < row.size(); x++)
        {
            if (row[x] == '#')
                grid.insert(Node({x, y}));
        }
        x = row.size();
        y++;
    }

    return std::make_pair(grid, Node({(x / 2), (y / 2)}));
}

static int partOne(std::pair<std::unordered_set<Node, NodeHasher>, Node>& grid)
{
    const uint iterations = 10'000;
    uint direction = 0;
    uint infections = 0;
    auto& [infected, carrier] = grid;

    for (uint burst = 0; burst < iterations; burst++)
    {
        if (infected.count(carrier))
        {
            direction = (direction + 3) % 4;
            infected.erase(carrier);
        }
        else
        {
            direction = (direction + 1) % 4;
            infected.insert(carrier);
            infections++;
        }
        carrier += const_cast<Node&>(unitVector[direction]);
    }

    return infections;
}

static int partTwo(std::pair<std::unordered_set<Node, NodeHasher>, Node>& grid)
{
    const uint iterations = 10'000'000;
    uint direction = 0;
    uint infections = 0;
    auto& [infected, carrier] = grid;
    std::unordered_set<Node, NodeHasher> weakened, flagged;

    for (uint burst = 0; burst < iterations; burst++)
    {
        if (weakened.count(carrier))
        {
            infected.insert(std::move(weakened.extract(carrier)));
            infections++;
        }
        else if (infected.count(carrier))
        {
            direction = (direction + 3) % 4;
            flagged.insert(std::move(infected.extract(carrier)));
        }
        else if (flagged.count(carrier))
        {
            direction = (direction + 2) % 4;
            flagged.erase(carrier);
        }
        else
        {
            direction = (direction + 1) % 4;
            weakened.insert(carrier);
        }
        carrier += const_cast<Node&>(unitVector[direction]);
    }

    return infections;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::pair<std::unordered_set<Node, NodeHasher>, Node> grid = readInput("input.txt");
    int result = (part == 1) ? partOne(grid) : partTwo(grid);
    std::cout << result << '\n';
    return 0;
}
