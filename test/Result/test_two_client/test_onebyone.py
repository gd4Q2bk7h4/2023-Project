import subprocess
import time

def run_client(script_name):
    """运行指定的客户端脚本，并记录执行时间"""
    start_time = time.perf_counter()  # 开始时间
    subprocess.run(["python", script_name])
    end_time = time.perf_counter()  # 结束时间
    print(f"{script_name} execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    # run_client('requst.py')
    
    # clients = ["./test_two_client/client1.py"]
    # clients = ["./test_two_client/client1.py", "./test_two_client/client2.py"]  # 客户端脚本列表
    # clients = ["./test_two_client/client1.py", "./test_two_client/client2.py","./test_two_client/client3.py"]  # 假设这是你的两个客户端脚本
    # clients = ["./test_two_client/client1.py", "./test_two_client/client2.py","./test_two_client/client3.py","./test_two_client/client4.py"]
    clients = ["./test_two_client/client1.py", "./test_two_client/client2.py","./test_two_client/client3.py","./test_two_client/client4.py","./test_two_client/client4.py"]
    
    start_time = time.time()
    for script in clients:
        run_client(script)
    end_time =time.time()
    print(f"Total execution time for all clients: {end_time-start_time:.2f} seconds")
