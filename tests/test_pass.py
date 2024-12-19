from .test import make_test

def test_pass(client, client2, password, server_name):
    print("\nPASS tests:\n")

    make_test(client2, f"PASS", f":{server_name} 461 * PASS :Not enough parameters")
    make_test(client2, "PASS wrong_pass", f":{server_name} 464 * :Password incorrect")
    client2.close()

    make_test(client, f"PASS {password}", None)