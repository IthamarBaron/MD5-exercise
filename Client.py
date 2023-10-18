# Client.py - Ithamar Baron
import hashlib
import math
import socket
import multiprocessing

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.cores = multiprocessing.cpu_count()
        self.work_range = None  # Store the assigned range
        self.TARGET = None # Store the md5 target
        self.sub_ranges = [] # Stores the sub ranges for each procces

    def connect_to_server(self):
        # Connect to the main server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to the server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Connection error: {str(e)}")

    def receive_work(self):
        # Receive the work range from the server
        work_info = self.client_socket.recv(1024).decode()
        print(f"receive_work -> {work_info}")
        work_info = work_info.split("-")
        self.work_range = [int(work_info[0]),int(work_info[1])]
        self.TARGET = work_info[2]

    def split_work(self):
        start_at, end_at = self.work_range
        jump_buffer = (end_at - start_at + 1) // self.cores  # Calculate the size of each sub-range

        core_start = start_at
        for core in range(1, self.cores + 1):
            core_end = core_start + jump_buffer - 1
            self.sub_ranges.append([core_start, core_end])  # Append the sub-range to the list
            core_start = core_end + 1
        print(self.sub_ranges)

    def generate_combinations(self, sub_work_range):
        # Generates the possible combinations in the work_range
        combinations = []
        i = sub_work_range[0]
        while i <= sub_work_range[1]:
            combinations.append(i)
            i += 1
        return combinations

    def crack_md5(self,combinations):
        for combination in combinations:
            if (hashlib.md5(str(combination).encode()).hexdigest() == self.TARGET):
                return combination
        return "No match found"

    def worker_function(self, sub_work_range,result_queue):
        # Perform MD5 cracking on the assigned sub-range
        print(f"worker SWR {sub_work_range}")
        combinations = self.generate_combinations(sub_work_range)
        result = self.crack_md5(combinations)
        result_queue.put(result)
        return result

    def distribute_work(self):
        # Create and start worker processes manually
        results = []
        processes = []
        result_queue = multiprocessing.Queue()

        # Create and start a process for each core
        for i in range(self.cores):
            process = multiprocessing.Process(target=self.worker_function, args=(self.sub_ranges[i], result_queue))
            processes.append(process)
            process.start()

        # Wait for all processes to finish
        for process in processes:
            process.join()

        # Get the results from the queue
        while not result_queue.empty():
            result = result_queue.get()
            results.append(result)

        print("Results:", results)
        self.send_result(results)

    def send_result(self, results):
        for result in results:
            if str(result) != "No match found":
                result_str = ("Match found! {" + str(result)  +"}")
                self.client_socket.send(result_str.encode())
                return
        self.client_socket.send("No match found!".encode())

        pass

if __name__ == "__main__":
    client = Client('172.16.5.10', 12345)
    client.connect_to_server()
    client.receive_work()
    client.split_work()
    client.distribute_work()
