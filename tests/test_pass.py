from .test import make_test

def test_pass(client, password, server_name, test_conn_generator):
    print("\nPASS tests:\n")


    client2 = test_conn_generator()
    make_test(client2, f"PASS", f":{server_name} 461 * PASS :Not enough parameters")
    client2.close()

    client2 = test_conn_generator()
    make_test(client2, "PASS wrong_pass", f":{server_name} 464 * :Password incorrect")
    client2.close()

    make_test(client, f"PASS {password}", None)