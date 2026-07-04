#include "Geometry.h"

#include <iostream>
#include <fstream>

std::pair<std::string, uint> RoutePacket(Map2D<char>& diagram)
{
    std::string letters;
    uint steps = 0;

    for (uint i = 0; i < diagram.GetWidth(); i++)
    {
        if (diagram[i, 0].value() == '|')
        {
            diagram.CreateEntity(i, 0, Map2D<char>::Entity::Orientation::SOUTH);
            break;
        }
    }

    Map2D<char>::Entity packet = diagram.GetEntity(0).value();
    std::optional<char> current, next;

    while (true)
    {
        current = packet.GetTile();
        steps++;
        if (current == std::nullopt)
            break;
        else if (current.value() == '+')
        {
            next = packet.Look(Map2D<char>::Entity::Direction::LEFT);
            if (next == std::nullopt || next.value() == ' ' || !packet.Move(Map2D<char>::Entity::Direction::LEFT))
                next = packet.Look(Map2D<char>::Entity::Direction::RIGHT);
            else
                continue;

            if (next == std::nullopt || next.value() == ' ' || !packet.Move(Map2D<char>::Entity::Direction::RIGHT))
                break;
        }
        else
        {
            if ((current.value() >= 'A') && (current.value() <= 'Z'))
                letters.append(1, current.value());

            if (!packet.Move(Map2D<char>::Entity::Direction::FRONT) || packet.GetTile().value() == ' ')
                break;
        }
    }

    return std::make_pair(letters, steps);
}

static Map2D<char> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<std::vector<char>> diagram;
    std::string line;
    while (getline(in, line)) {
        diagram.push_back(std::vector<char>(line.begin(), line.end()));
    }
    return Map2D<char>(diagram);
}

static std::string partOne(Map2D<char>& diagram)
{
    return RoutePacket(diagram).first;
}

static std::string partTwo(Map2D<char>& diagram)
{
    return std::to_string(RoutePacket(diagram).second);
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    Map2D<char> diagram = readInput("input.txt");
    std::string result = (part == 1) ? partOne(diagram) : partTwo(diagram);
    std::cout << result << '\n';
    return 0;
}
