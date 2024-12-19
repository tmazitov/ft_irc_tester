from client.client import connect_to_server, send_command
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
    
    client = connect_to_server(host, port)
    client2 = connect_to_server(host, port)

    # PASS
    test_pass(client, client2, password, server_name)
    client2.close()
    client2 = connect_to_server(host, port)
    send_command(client2, f"PASS {password}", True)

    try:
        # NICK
        test_nick(client, client2, "client_", server_name)

        # USER
        test_user(client, client2, "client_", "user_", server_name)

        # PRIVMSG
        test_privmsg(client, client2, "user_A", "client_1", "client_2", server_name)
    except Exception as e:
        print(e)

    # close connection
    client.close()
    client2.close()

if __name__ == "__main__":
    main()
