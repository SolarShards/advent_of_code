#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <unordered_map>

struct Program
{
    std::string name;
    uint weight;
    uint towerWeight;
    Program* holder;
    std::vector<Program*> held;

    Program(std::string n) : name(n), weight(0), towerWeight(0), holder(nullptr){}
    ~Program() { for (Program* p : held) delete p; }
    uint ComputeTowerWeight(void)
    {
        towerWeight = weight;
        for (Program* p : held)
            towerWeight += p->ComputeTowerWeight();
        return towerWeight;
    }
};

static Program* readInput(const std::string& path)
{
    Program* p;
    std::unordered_map<std::string, Program*> progs;
    std::ifstream file(path);
    std::string line;
    std::string token;

    while (getline(file, line)) {
        std::stringstream ss(line);

        ss >> token;
        if (!progs.count(token))
        {
            progs.insert({token, new Program(token)});
        }
        
        p = progs.at(token);

        ss >> token;
        p->weight = std::stoi(token.substr(1, token.size()-2));

        if (!(ss >> token))
            continue;

        while (ss >> token)
        {
            if (token.back() == ',')
                token.pop_back();
            if (!progs.count(token))
                progs.insert({token, new Program(token)});

            progs.at(token)->holder = p;
            p->held.push_back(progs.at(token));
        }
        
    }

    while (p->holder != nullptr)
        p = p->holder;

    p->ComputeTowerWeight();

    return p;
}

static std::string partOne(const Program* root)
{
    return root->name;
}

static uint partTwo(const Program* root)
{
    Program* node = const_cast<Program*>(root);
    std::unordered_map<uint, uint> weights; // weights : occurences
    uint wrongWeight;
    uint rightWeight;
    while (true)
    {
        weights.clear();
        wrongWeight = 0;

        for (Program* p : node->held)
        {
            if (!weights.count(p->towerWeight))
                weights.insert({p->towerWeight, 1});
            else
                weights[p->towerWeight]++;
        }

        if (weights.empty())
            return 0;

        if(weights.size() == 1)
            break;

        for (const auto& [w, count] : weights)
        {
            if (count == 1)
            {
                wrongWeight = w;
                break;
            }
        }

        if (!wrongWeight)
            return 0;

        for (Program* p : node->held)
        {
            if (p->towerWeight == wrongWeight)
            {
                node = p;
                break;
            }
        }
    }

    for (Program* p : node->holder->held)
    {
        if (p != node)
        {
            rightWeight = p->towerWeight;
            break;
        }
    }

    return node->weight + rightWeight - node->towerWeight;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    Program* root = readInput("input.txt");
    std::string result = (part == 1) ? partOne(root) : std::to_string(partTwo(root));
    std::cout << result << std::endl;
    return 0;
}
