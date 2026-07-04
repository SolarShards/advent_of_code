#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <regex>
#include <sstream>
#include <unordered_set>

static std::vector<std::string> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<std::string> passphrases;
    std::string line;
    while (getline(in, line)) {
        passphrases.push_back(line);
    }
    return passphrases;
}

static int partOne(const std::vector<std::string>& passphrases)
{
    int valid = 0;
    const std::regex r("\\b(\\w+)\\b.*\\b\\1\\b");
    for (auto p: passphrases)
        valid += static_cast<int>(!std::regex_search(p.data(), r));
    return valid;
}

static int partTwo(const std::vector<std::string>& passphrases)
{
    int valid = passphrases.size();
    for (auto p: passphrases)
    {
        std::unordered_set<std::string> words;
        std::stringstream ss(p);
        std::string word;
        
        while (ss >> word)
        {
            std::sort(word.begin(), word.end());
            if (words.count(word))
            {
                valid--;
                break;
            }
            words.insert(word);
        }
    }
    return valid;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<std::string> passphrases = readInput("input.txt");
    int result = (part == 1) ? partOne(passphrases) : partTwo(passphrases);
    std::cout << result << '\n';
    return 0;
}
