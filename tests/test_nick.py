from .test import make_test

def test_nick(client1, client2, nickname, server_name):
    print("\nNICK tests:\n")

    make_test(client1, "NICK", f":{server_name} 431 * :No nickname given")
    make_test(client1, f"NICK {nickname}", None)