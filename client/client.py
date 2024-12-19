import socket

# Make connection to server
def connect_to_server(host, port):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.settimeout(10) 
    return client_socket

# Send command to server and get response
def send_command(client_socket, command, without_response=False):
    client_socket.sendall(f"{command}\r\n".encode('utf-8'))
    if (without_response):
        return None
    response = ""
    try:
        response = client_socket.recv(4096).decode('utf-8')
    except TimeoutError:
        if without_response:
            return None
        return "TimeoutError"
    return response

