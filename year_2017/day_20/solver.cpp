#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <regex>
#include <vector>
#include <set>
#include <thread>

struct Particle
{
    int64_t position[3], velocity[3], acceleration[3];

    void Update()
    {
        for (uint8_t dim = 0; dim < 3; dim++)
        {
            velocity[dim] += acceleration[dim];
            position[dim] += velocity[dim];
        }
    }

    inline uint64_t Distance(const Particle& other) const
    {
        return std::abs(position[0] - other.position[0])
             + std::abs(position[1] - other.position[1])
             + std::abs(position[2] - other.position[2]);
    }

    inline bool Collides(const Particle& other) const
    {
        return (position[0] == other.position[0])
            && (position[1] == other.position[1])
            && (position[2] == other.position[2]);
    }
};

static std::vector<Particle> readInput(const std::string& path)
{
    std::vector<Particle> particles;
    std::ifstream in(path);
    std::string line;
    std::regex re("p=<(-?\\d+),(-?\\d+),(-?\\d+)>, v=<(-?\\d+),(-?\\d+),(-?\\d+)>, a=<(-?\\d+),(-?\\d+),(-?\\d+)>");
    std::smatch match;
    while (getline(in, line)) {
        if (std::regex_search(line, match, re) && match.size() == 10)
            particles.push_back({
                .position     = {std::stoi(match[1]), std::stoi(match[2]), std::stoi(match[3])},
                .velocity     = {std::stoi(match[4]), std::stoi(match[5]), std::stoi(match[6])},
                .acceleration = {std::stoi(match[7]), std::stoi(match[8]), std::stoi(match[9])},
            });
    }
    particles.shrink_to_fit();
    return particles;
}

static size_t partOne(std::vector<Particle>& particles)
{
    constexpr uint ticks = 1'000;
    const Particle origin = {.position = {0,0,0}, .velocity = {0,0,0}, .acceleration = {0,0,0}};
    std::vector<std::thread> threadpool;

    for (Particle& p : particles)
        threadpool.push_back(std::thread([&p, ticks](){ for (uint64_t t = 0; t < ticks; t++) p.Update(); }));

    for (std::thread& t : threadpool)
        t.join();

    auto closestToOrigin = std::min_element(
        particles.begin(), particles.end(),
        [&origin](const Particle& lhs, const Particle& rhs) { return lhs.Distance(origin) < rhs.Distance(origin); }
    );

    return std::distance(particles.begin(), closestToOrigin);
}

static size_t partTwo(std::vector<Particle>& particles)
{
    constexpr uint ticks = 1'000;
    std::set<size_t> toDelete;

    for (uint64_t t = 0; t < ticks; t++)
    {
        for (Particle& p : particles)
            p.Update();

        for (size_t i = 0; i < (particles.size() - 1); i++)
        {
            for (size_t j = i+1; j < particles.size(); j++)
            {
                if (particles[i].Collides(particles[j]))
                {
                    toDelete.insert(i);
                    toDelete.insert(j);
                }
            }
        }

        for (auto it = toDelete.rbegin(); it != toDelete.rend(); it++)
            particles.erase(particles.begin() + *it);
        toDelete.clear();
    }

    return particles.size();
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<Particle> particles = readInput("input.txt");
    size_t result = (part == 1) ? partOne(particles) : partTwo(particles);
    std::cout << result << '\n';
    return 0;
}
