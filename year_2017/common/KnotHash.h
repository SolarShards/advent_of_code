#include <array>
#include <numeric>
#include <vector>
#include <cstdint>
#include <string>

namespace std
{
    struct KnotHash
    {
    public:

        std::array<uint8_t, 16> operator()(const std::string& input)
        {
            std::array<uint8_t, 16> denseHash;
            std::array<uint8_t, 256> sparseHash;
            std::iota(sparseHash.begin(), sparseHash.end(), 0);
            std::vector<uint8_t> data(input.begin(), input.end());

            for (uint8_t i = 0; i < 64; i++)
            {
                SingleRound(sparseHash, data);
                SingleRound(sparseHash, KNOT_HASH_END_SEQUENCE);
            }

            for (uint8_t i = 0; i < 16; i++)
                denseHash[i] = std::accumulate(
                    sparseHash.begin() + 16 * i,
                    sparseHash.begin() + 16 * (i+1),
                    0, 
                    std::bit_xor<uint8_t>()
                );
            
            Reset();
            return denseHash;
        }

        void SingleRound(std::array<uint8_t, 256>& sequence, const std::vector<uint8_t>& data)
        {
            size_t size = sequence.size();
            int begin, end;

            for (uint length : data)
            {
                begin = position;
                end = (position + length - 1) % size;

                for (uint i = 0; i < length / 2; i++)
                {
                    std::swap(sequence[begin], sequence[end]);
                    begin = (begin + 1) % size;
                    end = (end - 1) % size;
                }

                position = (position + length + skip++) % size;
            }
        }

        void Reset(void)
        {
            position = 0;
            skip = 0;
        }

    private:
        int position = 0;
        uint skip = 0;
        static inline const std::vector<u_int8_t> KNOT_HASH_END_SEQUENCE = {17, 31, 73, 47, 23};
    };
}