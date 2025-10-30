# Basic HTTP Proxy Server

A simple, multi-threaded HTTP proxy server written in Python. It listens on a specified port and forwards HTTP requests from clients to target servers.

## Features
- Handles multiple client connections using threads
- Basic HTTP request forwarding
- Graceful shutdown with Ctrl+C
- Simple logging for requests and errors

## Requirements
- Python 3.x

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the proxy server:
   ```bash
   python proxy_server.py
   ```
2. Configure your browser or HTTP client to use `localhost:8888` as the HTTP proxy.

## Notes
- Only supports HTTP requests, not HTTPS.
- Designed for learning and testing purposes.
- Maximum simultaneous connections are defined by `MAX_CONN`.
- Buffer size for data transfer can be adjusted via `BUFFER_SIZE`.

## License
This project is licensed under the MIT License.
