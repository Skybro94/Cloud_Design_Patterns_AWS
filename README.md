# MySQL Cluster with Proxy and Gatekeeper

This project demonstrates a scalable and secure MySQL cluster using **Proxy** and **Gatekeeper** patterns on AWS.

## Features

- **Proxy Pattern**: Routes queries in three modes: 
  - `DIRECT_HIT`: All to manager.
  - `RANDOM`: Distributes among workers.
  - `CUSTOMIZED`: Routes based on latency.
- **Gatekeeper Pattern**: Adds a security layer for request validation.
- **Benchmarking**: Uses `sysbench` to test performance.

## Setup and Run

### 1. Clone the Repository
```bash
git clone https://github.com/Skybro94/Cloud_Design_Patterns_AWS.git
bash launch.sh
