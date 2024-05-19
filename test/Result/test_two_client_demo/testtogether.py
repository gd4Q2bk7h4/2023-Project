import concurrent.futures
import subprocess
import time

def run_client(script_name):
    """运行指定的客户端脚本"""
    print(time.time())
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    clients = ["client1.py", "client2.py"]  # 假设这是你的两个客户端脚本

    with concurrent.futures.ProcessPoolExecutor() as executor:
        start_time = time.perf_counter()  # 记录所有任务开始前的时间
        futures = [executor.submit(run_client, script) for script in clients]
        # 等待所有任务完成
        concurrent.futures.wait(futures)
        end_time = time.perf_counter()  # 记录所有任务完成后的时间

    total_time = end_time - start_time
    print(f"Total execution time for all clients: {total_time:.2f} seconds")
