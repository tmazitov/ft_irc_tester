from .test import make_test
from client.client import send_command

def test_user(clients, server_name):
    print("\nUSER tests:\n")

    # test not enough params
    make_test(clients[0].socket, f"USER",                             f":{server_name} 461 * USER :Not enough parameters")
    make_test(clients[0].socket, f"USER {clients[0].nickname}",       f":{server_name} 461 * USER :Not enough parameters")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0",     f":{server_name} 461 * USER :Not enough parameters")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 *",   f":{server_name} 461 * USER :Not enough parameters")

    # test wrong username
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :@{clients[0].username}", f":{server_name} 432 * :Erroneous username")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :#{clients[0].username}", f":{server_name} 432 * :Erroneous username")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :!{clients[0].username}", f":{server_name} 432 * :Erroneous username")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :&{clients[0].username}", f":{server_name} 432 * :Erroneous username")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :+{clients[0].username}", f":{server_name} 432 * :Erroneous username")
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :{clients[0].username}1a", f":{server_name} 432 * :Erroneous username")
    
    # test too long username
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :tooooooooooooooolong", f":{server_name} 432 * :Erroneous username")

    # test invalid nickname
    make_test(clients[0].socket, f"USER {clients[0].nickname}8 0 * :{clients[0].username}", None)
    
    # test valid nickname
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :{clients[0].username}", f":{server_name} 001 {clients[0].nickname} :Welcome to the IRC network")
    send_command(clients[1].socket, f"USER {clients[1].nickname} 0 * :{clients[1].username}")
    send_command(clients[2].socket, f"USER {clients[2].nickname} 0 * :{clients[2].username}")

    # test double execute USER
    make_test(clients[0].socket, f"USER {clients[0].nickname} 0 * :{clients[0].username}", f":{server_name} 462 * :You may not reregister")