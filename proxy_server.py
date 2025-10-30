import socket
import threading
import signal
import sys

# Configuration
LISTEN_PORT = 8888
MAX_CONN = 5
BUFFER_SIZE = 8192

# To keep track of running threads for graceful shutdown
threads = []
running = True

def handle_client(client_socket, client_address):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            client_socket.close()
            return

        # Parse HTTP request
        first_line = request.split(b'\n')[0]
        try:
            method, url, protocol = first_line.decode().split()
        except ValueError:
            client_socket.close()
            return

        # Extract host and port
        if "://" in url:
            url = url.split("://")[1]
        host_port = url.split("/")[0]
        if ":" in host_port:
            host, port = host_port.split(":")
            port = int(port)
        else:
            host = host_port
            port = 80

        print(f"[INFO] Forwarding request from {client_address} to {host}:{port}")

        # Connect to target server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, port))
        server_socket.sendall(request)

        while True:
            data = server_socket.recv(BUFFER_SIZE)
            if len(data) > 0:
                client_socket.send(data)
            else:
                break

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client_socket.close()
        server_socket.close()


def start_server():
    global running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", LISTEN_PORT))
    server_socket.listen(MAX_CONN)
    print(f"[INFO] Proxy server listening on port {LISTEN_PORT}...")

    while running:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            threads.append(client_thread)
        except KeyboardInterrupt:
            print("\n[INFO] Shutting down proxy server...")
            running = False
            break
        except Exception as e:
            print(f"[ERROR] {e}")

    server_socket.close()
    for t in threads:
        t.join()
    print("[INFO] Server stopped.")


if __name__ == "__main__":
    start_server()
