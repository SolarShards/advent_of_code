#include <cstdint>
#include <functional>
#include <iostream>
#include <fstream>
#include <string>
#include <thread>
#include <utility>
#include <regex>
#include <stdexcept>
#include <mutex>
#include <queue>
#include <condition_variable>

class Generator
{
public:
    Generator(uint64_t seed, uint64_t factor, uint64_t criteria)
    : _value(seed), _factor(factor), _criteria(criteria) {}

    uint64_t Generate(void)
    {
        _value = (_value * _factor) % INT32_MAX;
        return _value;
    }

    uint64_t GenerateMatchingCriteria(void)
    {
        while ((_value = (_value * _factor) % INT32_MAX) % _criteria);
        return _value;
    }

private:
    uint64_t _value;
    uint64_t _factor;
    uint64_t _criteria;
};

static constexpr uint64_t factorA = 16807;
static constexpr uint64_t factorB = 48271;
static constexpr uint64_t criteriaA = 4;
static constexpr uint64_t criteriaB = 8;

static std::pair<Generator, Generator> readInput(const std::string& path)
{
    uint64_t seedA, seedB;
    std::ifstream in(path);
    std::string line;
    std::regex re("\\d+");
    std::smatch match;

    getline(in, line);
    if (!std::regex_search(line, match, re))
        throw std::invalid_argument("Could not get seed of generator A");
    seedA = std::stoi(match.str());

    getline(in, line);
    if (!std::regex_search(line, match, re))
        throw std::invalid_argument("Could not get seed of generator B");
    seedB = std::stoi(match.str());

    return std::pair<Generator, Generator>(Generator(seedA, factorA, criteriaA), Generator(seedB, factorB, criteriaB));
}

static int partOne(Generator& a, Generator& b)
{
    constexpr uint64_t iterations = 40'000'000;
    uint64_t matches = 0;

    for(uint64_t i = 0; i < iterations; i++)
        matches += static_cast<uint64_t>(static_cast<uint16_t>(a.Generate()) == static_cast<uint16_t>(b.Generate()));

    return matches;
}

static int partTwo(Generator& a, Generator& b)
{
    constexpr uint64_t iterations = 5'000'000;
    uint64_t matches = 0;

    std::mutex mutex;
    std::queue<uint64_t> queueA, queueB;
    std::condition_variable condition;
    bool run = true;
    auto f = [&](Generator& gen, std::queue<uint64_t>& queue){
        for(uint64_t count = 0; count < iterations; count++)
        {
            uint64_t value = gen.GenerateMatchingCriteria();
            std::lock_guard<std::mutex> lock(mutex);
            queue.push(value);
            condition.notify_one();
        }
    };

    std::thread thread_a(f, std::ref(a), std::ref(queueA));
    std::thread thread_b(f, std::ref(b), std::ref(queueB));

    for(uint64_t i = 0; i < iterations; i++)
    {
        std::unique_lock<std::mutex> lock(mutex);
        condition.wait(lock, [&]() { return !queueA.empty() && !queueB.empty(); });
        matches += static_cast<uint64_t>(static_cast<uint16_t>(queueA.front()) == static_cast<uint16_t>(queueB.front()));
        queueA.pop();
        queueB.pop();
    }

    thread_a.join();
    thread_b.join();

    return matches;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::pair<Generator, Generator> g = readInput("input.txt");
    int result = (part == 1) ? partOne(g.first, g.second) : partTwo(g.first, g.second);
    std::cout << result << '\n';
    return 0;
}
