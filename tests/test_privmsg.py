from .test import make_test

def test_privmsg(client):
    print("\nPRIVMSG tests:\n")

    make_test(client, "PRIVMSG notfound :user not found", "OK")