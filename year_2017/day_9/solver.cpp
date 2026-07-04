#include <cstddef>
#include <iostream>
#include <fstream>
#include <string>

static std::string readInput(const std::string& path)
{
    std::ifstream in(path);
    std::string stream;
    in >> stream;
    return stream;
}

static void cleanCanceled(std::string& stream)
{
    size_t c;
    while((c = stream.find('!')) != std::string::npos)
        stream.erase(c, 2);
}

static uint cleanGarbage(std::string& stream)
{
    uint count = 0;
    size_t start, end;
    while((start = stream.find('<')) != std::string::npos)
    {
        end = stream.find('>', start);
        stream.erase(start, end - start + 1);
        count += end - start + 1 - 2;
    }
    return count;
}

static int partOne(std::string& stream)
{
    cleanCanceled(stream);
    cleanGarbage(stream);

    uint score = 0;
    uint total = 0;

    for (char c : stream)
    {
        if (c == '{') score++;
        if (c == '}')
            total += score--;
    }
    return total;
}

static int partTwo(std::string& stream)
{
    cleanCanceled(stream);
    return cleanGarbage(stream);
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::string stream = readInput("input.txt");
    int result = (part == 1) ? partOne(stream) : partTwo(stream);
    std::cout << result << '\n';
    return 0;
}
