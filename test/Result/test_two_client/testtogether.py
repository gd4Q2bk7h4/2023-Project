import concurrent.futures
import subprocess
import time

def run_client(script_name):
    """运行指定的客户端脚本"""
    print(time.time())
    subprocess.run(["python", script_name])

if __name__ == "__main__":
    # run_client('./test_two_client/requst.py')
    # clients = ["./test_two_client/client1.py"]
    clients = ["./test_two_client/client1.py", "./test_two_client/client2.py"]  # 假设这是你的两个客户端脚本
    # clients = ["./test_two_client/client1.py", "./test_two_client/client2.py","./test_two_client/client3.py","./test_two_client/client4.py"]
    # clients = ["./test_two_client/client1.py", "./test_two_client/client2.py","./test_two_client/client3.py","./test_two_client/client4.py","./test_two_client/client4.py"]
    start_time = time.time()  # 记录所有任务开始前的时间
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(run_client, script) for script in clients]
        # 等待所有任务完成
        concurrent.futures.wait(futures)
        
    end_time = time.time()  # 记录所有任务完成后的时间
    print(f"Total execution time for all clients: {end_time - start_time:.2f} seconds")
