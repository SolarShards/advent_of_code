
#include <optional>
#include <functional>
#include <mdspan>
#include <stdexcept>
#include <unordered_map>
#include <utility>
#include <vector>

#define DIRECTIONS 8

template <typename TileType>
class Map2D
{
public:
    class Entity
    {
    public:
        struct Position 
        {
            int x, y;
            Position operator+(const Position& other) const
            {
                return Position(x + other.x, y + other.y);
            }
            Position& operator+=(const Position& other)
            {
                x += other.x;
                y += other.y;
                return *this;
            }
        };
        enum Orientation {
            EAST = 0,
            NORTH_EAST = 1,
            NORTH = 2,
            NORTH_WEST = 3,
            WEST = 4,
            SOUTH_WEST = 5,
            SOUTH = 6 ,
            SOUTH_EAST = 7
        };
        static inline std::unordered_map<Orientation, Position> unitVectors = {
            { EAST,       {+1, +0} },
            { NORTH_EAST, {+1, -1} },
            { NORTH,      {+0, -1} },
            { NORTH_WEST, {-1, -1} },
            { WEST,       {-1, +0} },
            { SOUTH_WEST, {-1, +1} },
            { SOUTH,      {+0, +1} },
            { SOUTH_EAST, {+1, +1} }
        };
        enum Direction {
            FRONT = 0,
            FRONT_LEFT = 1,
            LEFT = 2,
            BACK_LEFT = 3,
            BACK = 4,
            BACK_RIGHT = 5,
            RIGHT = 6 ,
            FRONT_RIGHT = 7
        };

        Entity(
            Map2D<TileType>& map,
            const uint x = 0, const uint y = 0, const Orientation o = EAST)
        : _map(const_cast<Map2D<TileType>&>(map))
        {
            if (!PlaceOnMap(map, x, y, o))
                throw std::out_of_range("Wrong coordinates");
        }

        bool PlaceOnMap(
            Map2D<TileType>& map,
            const uint x = 0, const uint y = 0, const Orientation o = EAST)
        {
            if (map[x, y] == std::nullopt)
                return false;
            _map = map;
            _position = {static_cast<int>(x), static_cast<int>(y)};
            _orientation = o;
            return true;
        }

        inline std::optional<std::reference_wrapper<TileType>> Look(const Orientation orientation) const
        {
            return _map[_position + unitVectors[orientation]];
        }

        inline std::optional<std::reference_wrapper<TileType>> Look(const Direction direction) const
        {
            return _map[_position + unitVectors[static_cast<Orientation>(((int)_orientation + (int)direction) % DIRECTIONS)]];
        }

        bool Move(const Orientation orientation)
        {
            Position p = Look(orientation);
            if (p == std::nullopt)
                return false;
            _position = p;
            _orientation = orientation;
            return true;
        }

        bool Move(const Direction direction)
        {
            if (Look(direction) == std::nullopt)
                return false;
            _orientation = static_cast<Orientation>(((int)_orientation + (int)direction) % DIRECTIONS);
            _position += unitVectors[_orientation];
            return true;
        }

        bool Move(const Position position, const std::optional<Orientation> orientation)
        {
            if (_map)
                return false;
            _position = position;
            if (orientation != std::nullopt)
                _orientation = orientation;
            return true;
        }

        void Rotate(const Direction direction)
        {
            _orientation = (_orientation + direction) % DIRECTIONS;
        }

        const Position& GetPosition() { return _position; }
        std::optional<TileType> GetTile() { return _map[_position]; }

    protected:

        Position _position;
        Orientation _orientation;
        Map2D<TileType>& _map;
    };

    Map2D(const std::vector<TileType>& map, const uint rows, const uint columns) : _data(map), _span(_data.data(), rows, columns){}

    Map2D(std::vector<TileType>&& map, const uint rows, const uint columns) : _data(std::move(map)), _span(_data.data(), rows, columns){}

    Map2D(std::vector<std::vector<TileType>>& map)
    {
        for (std::vector<TileType>& row : map)
            _data.insert(_data.end(), row.begin(), row.end());
        _span = std::mdspan<TileType, std::dextents<size_t, 2>>(_data.data(), map.size(), map.at(0).size());
    }

    template <auto R, auto C>
    Map2D(const std::array<std::array<TileType, C>, R>& map)
    {
        for (std::array<TileType, C>&& row : map)
            _data.insert(_data.end(), row.begin(), row.end());
        _span = std::mdspan<TileType, std::dextents<size_t, 2>>(_data.data(), R, C);
    }

    std::optional<std::reference_wrapper<TileType>> operator[](uint x, uint y)
    {
        if ((x < GetWidth()) || (y < GetHeight()))
            return std::ref(_span[y, x]);
        else
            return std::nullopt;
    }

    std::optional<std::reference_wrapper<TileType>> operator[](Entity::Position p)
    {
        if ((p.x >= 0) && (p.x < GetWidth()) && (p.y >= 0) && (p.y < GetHeight()))
            return std::ref(_span[p.y, p.x]);
        else 
            return std::nullopt;
    }

    uint GetHeight() { return _span.extent(0); }
    uint GetWidth() { return _span.extent(1); }

    uint CreateEntity(const uint x = 0, const uint y = 0, const Entity::Orientation o = Entity::Orientation::EAST)
    {
        uint id = _entities.size();
        _entities.insert({id, Entity(*this, x, y, o)});
        return id;
    }

    std::optional<std::reference_wrapper<Entity>> GetEntity(uint id)
    {
        if (_entities.count(id))
            return std::ref(_entities.at(id));
        else
            return std::nullopt;
    }

protected:
    std::vector<TileType> _data;
    std::mdspan<TileType, std::dextents<size_t, 2>> _span;
    std::unordered_map<uint, Entity> _entities;
};
