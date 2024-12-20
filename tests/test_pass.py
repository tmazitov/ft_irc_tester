from .test import make_test
from client.client import send_command

def test_pass(clients, password, server_name):
    print("\nPASS tests:\n")

    make_test(clients[1].socket, f"PASS", f":{server_name} 461 * PASS :Not enough parameters")
    make_test(clients[1].socket, "PASS wrong_pass", f":{server_name} 464 * :Password incorrect")
    clients[1].close()

    make_test(clients[0].socket, f"PASS {password}", None)
    send_command(clients[2].socket, f"PASS {password}", None)