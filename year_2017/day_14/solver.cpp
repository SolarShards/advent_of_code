#include "KnotHash.h"
#include <array>
#include <bitset>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <numeric>
#include <string>
#include <unordered_set>

#define GRID_SIZE 128

template <size_t rows, size_t cols> class Disk : public std::array<std::bitset<cols>, rows>
{
private:
    struct Square 
    {
        uint64_t row, col;

        inline bool operator==(const Square& other) const
        {
            return (row == other.row) && (col == other.col);
        }
    };

    struct SquareHasher {
        size_t operator()(const Square& s) const
        {
            return std::hash<uint64_t>()(s.row) ^ (std::hash<uint64_t>()(s.col) << 1);
        }
    };

public:
    inline uint UsedSpace(void) const
    {
        return std::accumulate(this->begin(), this->end(), 0, [](uint sum, const std::bitset<cols> row) { return sum + row.count(); });
    }

    inline void DeleteRegion(uint64_t startRow, uint64_t startCol)
    {
        (*this)[startRow][startCol] = 0;
        std::unordered_set<Square, SquareHasher> toScan = {{startRow, startCol}};

        while(!toScan.empty())
        { 
            std::unordered_set<Square, SquareHasher> next;
            for (auto it = toScan.begin(); it != toScan.end(); it++)
            {
                if ((it->row > 0) && ((*this)[it->row - 1][it->col] == 1))
                {
                    next.insert({it->row - 1, it->col});
                    (*this)[it->row - 1][it->col] = 0;
                }

                if ((it->row < (rows - 1)) && ((*this)[it->row + 1][it->col] == 1))
                {
                    next.insert({it->row + 1, it->col});
                    (*this)[it->row + 1][it->col] = 0;
                }

                if ((it->col > 0) && ((*this)[it->row][it->col - 1] == 1))
                {
                    next.insert({it->row, it->col - 1});
                    (*this)[it->row][it->col - 1] = 0;
                }

                if ((it->col < (cols - 1)) && ((*this)[it->row][it->col + 1] == 1))
                {
                    next.insert({it->row, it->col + 1});
                    (*this)[it->row][it->col + 1] = 0;
                }
            }
            
            toScan = std::move(next);
        }
    }

    inline uint CountRegions(void) const
    {
        uint count = 0;
        Disk<rows, cols> memMap = *this;

        for (size_t r = 0; r < rows; r++)
        {
            for (size_t c = 0; c < cols; c++)
            {
                if (memMap[r][c] == 1)
                {
                    memMap.DeleteRegion(r, c);
                    count++;
                }
            }
        }

        return count;
    }
};

static Disk<GRID_SIZE, GRID_SIZE> readInput(const std::string& path)
{
    Disk<GRID_SIZE, GRID_SIZE> disk;
    std::KnotHash hashFunction;
    std::ifstream in(path);
    std::string input;
    in >> input;

    for (uint i = 0; i < GRID_SIZE; i++)
    {
        std::array<uint8_t, 16> hash = hashFunction(input + '-' + std::to_string(i));
        for (uint8_t j = 0; j < 16; j++)
        {
            disk[i] |= std::bitset<GRID_SIZE>(hash[j]) << (8 * (15 - j));
        }
    }

    return disk;
}

static uint partOne(const Disk<GRID_SIZE, GRID_SIZE>& disk)
{
    return disk.UsedSpace();
}

static uint partTwo(const Disk<GRID_SIZE, GRID_SIZE>& disk)
{
    return disk.CountRegions();
}

int main(int argc, char** argv)
{
    int part = std::stoi(argv[1]);
    Disk<GRID_SIZE, GRID_SIZE> disk = readInput("input.txt");
    uint result = (part == 1) ? partOne(disk) : partTwo(disk);
    std::cout << result << '\n';
    return 0;
}
