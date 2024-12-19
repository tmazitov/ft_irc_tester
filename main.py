from client.client import connect_to_server, send_command
from tests.test_privmsg import test_privmsg
from tests.test_pass import test_pass
from sys import argv

def make_test_conn():
    host = argv[1]
    port = int(argv[2])

    return connect_to_server(host, port)

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
    
    client = connect_to_server(host, port)

    # some tests
    test_pass(client, password, server_name, make_test_conn, True)

    # close connection
    client.close()

if __name__ == "__main__":
    main()
