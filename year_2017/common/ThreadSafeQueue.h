#include <queue>
#include <mutex>
#include <condition_variable>

template<typename T>
class ThreadSafeQueue: public std::queue<T>
{
public:
    void ThreadSafePush(const T& value)
    {
        std::lock_guard<std::mutex> lock(mutex);
        std::queue<T>::push(value);
        condition.notify_one();
    }

    T ThreadSafePop()
    {
        std::unique_lock<std::mutex> lock(mutex);
        condition.wait(lock, [this](){ return !this->empty(); });
        T ret = std::queue<T>::front();
        std::queue<T>::pop();
        return ret;
    }

    void clear()
    {
        while (!std::queue<T>::empty())
            std::queue<T>::pop();
    }

private:
    std::mutex mutex;
    std::condition_variable condition;
};