from evalscope.perf.arguments import Arguments
from evalscope.perf.main import run_perf_benchmark
from rich import print

if __name__ == "__main__":
    args = Arguments(
        url="http://localhost:8082/v1/chat/completions",  # Requested URL address
        parallel=100,  # Number of parallel request tasks
        model="qwen",  # Model name used
        number=100,  # Number of requests
        api="openai",  # API service used
        dataset="openqa",  # Dataset name
        stream=True,  # Whether to enable streaming
    )
    run_perf_benchmark(args)
    print(
        "To understand the meaning of metrics, please visit: https://evalscope.readthedocs.io/zh-cn/latest/user_guides/stress_test/quick_start.html"
    )
