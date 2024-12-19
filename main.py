from client.client import connect_to_server, send_command, Client
from tests.test_privmsg import test_privmsg
from tests.test_pass import test_pass
from tests.test_nick import test_nick
from tests.test_user import test_user
from sys import argv

def main():

    if len(argv) != 5:
        print("Usage: python main.py <host> <port> <password> <server_name>")
        exit(1)

    if not argv[2].isnumeric():
        print("Port must be a number")
        exit(1)

    # setup connection

    host = argv[1]
    port = int(argv[2])
    password = argv[3]
    server_name = argv[4]
    
    clients = [
        Client(host, port, "client1", "One"),
        Client(host, port, "client2", "Two"),
        Client(host, port, "client3", "Three"),
    ]

    # PASS
    test_pass(clients, password, server_name)
    clients[1].socket = connect_to_server(host, port)
    send_command(clients[1].socket, f"PASS {password}", True)

    try:
        # NICK
        test_nick(clients, server_name)

        # USER
        test_user(clients, server_name)

        # PRIVMSG
        test_privmsg(clients, server_name)
    except Exception as e:
        print(e)

    # close connection
    for client in clients:
        client.close()

if __name__ == "__main__":
    main()
