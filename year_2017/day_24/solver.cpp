#include <algorithm>
#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>

struct Component
{
    uint id, left, right;
    bool operator==(const Component& other) { return id == other.id; }
};

static std::vector<std::vector<Component>> createAllBridges(const std::vector<Component>& components)
{
    std::vector<std::vector<Component>> completedBridges, inProgress;
    for (Component c : components)
    {
        if (c.right == 0)
            std::swap(c.left, c.right);

        if (c.left == 0)
            inProgress.push_back({c});
    }

    while (!inProgress.empty())
    {
        std::vector<std::vector<Component>> next;
        for (std::vector<Component>& bridge : inProgress)
        {
            if (bridge.size() == components.size())
                continue;

            for (Component c : components)
            {
                if (c.right == bridge.back().right)
                    std::swap(c.left, c.right);

                if (std::find(bridge.begin(), bridge.end(), c) != bridge.end())
                    continue;

                if (c.left == bridge.back().right)
                {
                    std::vector<Component> newBridge(bridge);
                    newBridge.push_back(c);
                    next.push_back(newBridge);
                }
            }

        }
        std::move(inProgress.begin(), inProgress.end(), std::back_inserter(completedBridges));
        inProgress.clear();
        std::move(next.begin(), next.end(), std::back_inserter(inProgress));
    }

    return completedBridges;
}

static std::vector<Component> readInput(const std::string& path)
{
    std::ifstream in(path);
    std::vector<Component> components;
    std::string line;
    uint id = 0;
    while (getline(in, line)) {
        components.push_back({
            .id = id,
            .left = static_cast<uint>(std::stoi(line.substr(0,line.find('/')))),
            .right = static_cast<uint>(std::stoi(line.substr(line.find('/')+1)))
        });
        id++;
    }
    return components;
}

static int partOne(const std::vector<Component>& components)
{
    uint strongest = 0;
    std::vector<std::vector<Component>> completedBridges = createAllBridges(components);

    for (std::vector<Component>& bridge : completedBridges)
    {
        uint strength = 0;
        for (Component& c : bridge)
            strength += c.left + c.right;
        strongest = std::max(strength, strongest);
    }

    return strongest;
}

static int partTwo(const std::vector<Component>& components)
{
    uint strongestAmongLongest = 0;
    std::vector<std::vector<Component>> completedBridges = createAllBridges(components);

    for (auto it = completedBridges.rbegin(); (it != completedBridges.rend()) && (it->size() == completedBridges.rbegin()->size()); it++)
    {
        uint strength = 0;
        for (Component& c : *it)
            strength += c.left + c.right;
        strongestAmongLongest = std::max(strength, strongestAmongLongest);
    }

    return strongestAmongLongest;
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    std::vector<Component> components = readInput("input.txt");
    int result = (part == 1) ? partOne(components) : partTwo(components);
    std::cout << result << '\n';
    return 0;
}
