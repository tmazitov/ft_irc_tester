from .test import make_test
from client.client import send_command

def test_nick(clients, server_name):
    print("\nNICK tests:\n")

    # test without nickname
    make_test(clients[0].socket, "NICK", f":{server_name} 431 * :No nickname given")
    
    # test with invalid nickname
    make_test(clients[0].socket, f"NICK @{clients[0].nickname}", f":{server_name} 432 * @{clients[0].nickname} :Erroneous nickname")
    make_test(clients[0].socket, f"NICK #{clients[0].nickname}", f":{server_name} 432 * #{clients[0].nickname} :Erroneous nickname")
    make_test(clients[0].socket, f"NICK !{clients[0].nickname}", f":{server_name} 432 * !{clients[0].nickname} :Erroneous nickname")
    make_test(clients[0].socket, f"NICK &{clients[0].nickname}", f":{server_name} 432 * &{clients[0].nickname} :Erroneous nickname")
    make_test(clients[0].socket, f"NICK +{clients[0].nickname}", f":{server_name} 432 * +{clients[0].nickname} :Erroneous nickname")

    # test with busy nickname
    send_command(clients[1].socket, f"NICK {clients[1].nickname}")
    send_command(clients[2].socket, f"NICK {clients[2].nickname}")
    make_test(clients[0].socket, f"NICK {clients[0].nickname}", f":{server_name} 433 * {clients[0].nickname} :Nickname is already in use")

    # test with valid nickname
    make_test(clients[0].socket, f"NICK {clients[0].nickname}", None)