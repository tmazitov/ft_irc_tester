import socket
import threading
from sys import argv

lock = threading.Lock()

def receive_handler(client_socket):
    """Function to listen to server messages."""
    while True:
        with lock:
            try:
                data = client_socket.recv(4096)  # Receive up to 4 KB
                if not data:
                    print("❌ Server disconnected.")
                    break
                print(f"📩 {data.decode('utf-8')}")
            except TimeoutError:
                continue  # Ignore timeout, keep listening
            except (ConnectionResetError, OSError):
                print("❌ Connection lost.")
                break
    client_socket.close()

def send_handler(client_socket):
    """Function to handle user input and send commands to the server."""
    while True:
        user_input = input("Enter command ('q' to quit): ")
        if user_input == "q":
            print("❌ Disconnecting...")
            break
        try:
            # Log the command being sent
            print(f"Sending command: {user_input}")
            client_socket.sendall(f"{user_input}\r\n".encode('utf-8'))
        except (ConnectionResetError, OSError) as e:
            print(f"❌ Failed to send message. Error: {e}")
            break
    client_socket.close()


def connect_to_server(host, port):
    """Establish connection to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.settimeout(3)  # Set timeout to 3 seconds
    return client_socket

def main():
    if len(argv) != 6:
        print("Usage: python main.py <host> <port> <password> <nickname> <username>")
        exit(1)

    host = argv[1]
    if not argv[2].isdigit():
        print("❌ Port must be a number.")
        exit(1)
    port = int(argv[2])
    password = argv[3]
    nickname = argv[4]
    username = argv[5]

    try:
        client = connect_to_server(host, port)
    except ConnectionRefusedError:
        print("❌ Error: Unable to connect to server.")
        exit(1)

    print("✅ Connected to server.")

    # Authenticate with server
    try:
        client.sendall(f"PASS {password}\r\n".encode('utf-8'))
        client.sendall(f"NICK {nickname}\r\n".encode('utf-8'))
        client.sendall(f"USER {nickname} 0 * :{username}\r\n".encode('utf-8'))
    except (ConnectionResetError, OSError):
        print("❌ Error: Unable to authenticate.")
        client.close()
        exit(1)

    print("✅ Authentication successful. Ready to use.")

    # Start threads for sending and receiving
    receive_thread = threading.Thread(target=receive_handler, args=(client,))
    send_thread = threading.Thread(target=send_handler, args=(client,))
    receive_thread.start()
    send_thread.start()

    # Wait for threads to finish
    send_thread.join()
    receive_thread.join()
    print("✅ Client disconnected.")

if __name__ == "__main__":
    main()
