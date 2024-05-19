import subprocess
import time

def run_client(script_name):
    """运行指定的客户端脚本，并记录执行时间"""
    start_time = time.perf_counter()  # 开始时间
    subprocess.run(["python", script_name])
    end_time = time.perf_counter()  # 结束时间
    print(f"{script_name} execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    start_time = time.time()
    client_scripts = ["client1.py", "client2.py"]  # 客户端脚本列表

    for script in client_scripts:
        run_client(script)
    end_time =time.time()
    print(f"Total execution time for all clients: {end_time-start_time:.2f} seconds")
