#모듈 설치 pip3 install pytest-benchmark

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def test_fibonacci_recursive_benchmark(benchmark):
    result = benchmark.pedantic(fibonacci, args=(20,), rounds=10)
    assert result == 6765

def test_fibonacci_iterative_benchmark(benchmark):
    result = benchmark.pedantic(fibonacci_iterative, args=(20,), rounds=10)
    assert result == 6765
