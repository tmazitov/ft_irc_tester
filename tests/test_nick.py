from .test import make_test
from client.client import send_command

def test_nick(client1, client2, nickname, server_name):
    print("\nNICK tests:\n")

    # test without nickname
    make_test(client1, "NICK", f":{server_name} 431 * :No nickname given")
    
    # test with invalid nickname
    make_test(client1, f"NICK @{nickname}", f":{server_name} 432 * @{nickname} :Erroneous nickname")
    make_test(client1, f"NICK #{nickname}", f":{server_name} 432 * #{nickname} :Erroneous nickname")
    make_test(client1, f"NICK !{nickname}", f":{server_name} 432 * !{nickname} :Erroneous nickname")
    make_test(client1, f"NICK &{nickname}", f":{server_name} 432 * &{nickname} :Erroneous nickname")
    make_test(client1, f"NICK +{nickname}", f":{server_name} 432 * +{nickname} :Erroneous nickname")

    # test with busy nickname
    send_command(client2, f"NICK {nickname}1")
    make_test(client1, f"NICK {nickname}1", f":{server_name} 433 * {nickname}1 :Nickname is already in use")

    # test with valid nickname
    make_test(client1, f"NICK {nickname}", None)