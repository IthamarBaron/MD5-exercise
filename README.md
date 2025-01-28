# Distributed MD5 Hash Cracker

## Overview
This project demonstrates a distributed computing approach to MD5 hash cracking using Python. It features a client-server model to divide and conquer the task of brute-forcing hashes.

## Features
- **Client-Server Model**: Server distributes tasks to connected clients.
- **Parallel Processing**: Clients utilize all CPU cores for efficient computation.
- **MD5 Hash Cracking**: Clients brute-force numeric combinations to find a match.
- **Dynamic Task Allocation**: Workload is divided among clients dynamically.

## Technical Highlights
- **Multiprocessing**: Clients use multiple processes for sub-range computation.
- **Distributed Computing**: Work is shared across multiple machines.
- **Socket Communication**: Server-client communication with Python sockets.
- **Hashing**: MD5 hashing using Python's `hashlib`.

## How It Works
1. **Server**: Accepts clients, takes target hash and range, distributes tasks, and collects results.
2. **Client**: Connects to server, processes assigned range, and returns results.

## Usage
1. Run the server:
   ```bash
   python Server.py
   ```
   Enter number of clients, target MD5 hash, and range.
2. Run the clients:
   ```bash
   python Client.py
   ```
3. View results on the server.

## Educational Value
This project highlights parallel and distributed computing concepts, socket programming, and MD5 hashing.


