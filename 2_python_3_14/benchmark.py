"""
Python 3.13 vs 3.14t (Free-threaded) 벤치마크
CPU 집약적 작업에서의 멀티스레드 성능 비교
"""
import time
import math
import sys
from concurrent.futures import ThreadPoolExecutor


def cpu_heavy_work(n):
    """CPU 집약적 작업 - factorial 계산"""
    total = 0
    for i in range(n):
        total += math.factorial(100)
    return total


def benchmark_single_thread(iterations=500_000, workers=4):
    """싱글 스레드 벤치마크"""
    print(f"\n[싱글 스레드] {workers}개의 작업을 순차 실행")
    start = time.perf_counter()
    
    results = []
    for i in range(workers):
        results.append(cpu_heavy_work(iterations))
    
    elapsed = time.perf_counter() - start
    print(f"소요 시간: {elapsed:.2f}초")
    return elapsed


def benchmark_multi_thread(iterations=500_000, workers=4):
    """멀티 스레드 벤치마크"""
    print(f"\n[멀티 스레드] {workers}개의 스레드로 병렬 실행")
    start = time.perf_counter()
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(cpu_heavy_work, iterations) for _ in range(workers)]
        results = [f.result() for f in futures]
    
    elapsed = time.perf_counter() - start
    print(f"소요 시간: {elapsed:.2f}초")
    return elapsed


def check_gil_status():
    """GIL 상태 확인"""
    try:
        # Python 3.13+에서 사용 가능
        if hasattr(sys, '_is_gil_enabled'):
            return "Disabled (Free-threaded)" if not sys._is_gil_enabled() else "Enabled"
        else:
            return "Enabled (확인 불가)"
    except:
        return "Enabled"


def main():
    print("=" * 60)
    print("Python 멀티스레드 벤치마크")
    print("=" * 60)
    print(f"Python 버전: {sys.version.split()[0]}")
    print(f"GIL 상태: {check_gil_status()}")
    print(f"CPU 코어 수: {ThreadPoolExecutor()._max_workers}")
    print("=" * 60)
    
    # 워커 수 설정
    workers = 4
    iterations = 500_000
    
    # 벤치마크 실행
    single_time = benchmark_single_thread(iterations, workers)
    multi_time = benchmark_multi_thread(iterations, workers)
    
    # 결과 출력
    print("\n" + "=" * 60)
    print("결과 요약")
    print("=" * 60)
    print(f"싱글 스레드: {single_time:.2f}초")
    print(f"멀티 스레드: {multi_time:.2f}초")
    
    speedup = single_time / multi_time
    print(f"\n속도 향상: {speedup:.2f}x")
    
    if speedup > 2.0:
        print("✅ Free-threading 효과 확인! (GIL 제거)")
    elif speedup < 1.2:
        print("❌ GIL로 인해 병렬화 효과 없음")
    else:
        print("⚠️  부분적인 성능 향상")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
