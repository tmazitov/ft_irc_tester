from .test import make_test

def test_user(client, client2, nickname, username, server_name):
    print("\nUSER tests:\n")

    # test not enough params
    make_test(client, f"USER",                  f":{server_name} 461 * USER :Not enough parameters")
    make_test(client, f"USER {nickname}",       f":{server_name} 461 * USER :Not enough parameters")
    make_test(client, f"USER {nickname} 0",     f":{server_name} 461 * USER :Not enough parameters")
    make_test(client, f"USER {nickname} 0 *",   f":{server_name} 461 * USER :Not enough parameters")

    # test wrong username
    make_test(client, f"USER {nickname}1 0 * :@{username}", f":{server_name} 432 * :Erroneous username")
    make_test(client, f"USER {nickname}1 0 * :#{username}", f":{server_name} 432 * :Erroneous username")
    make_test(client, f"USER {nickname}1 0 * :!{username}", f":{server_name} 432 * :Erroneous username")
    make_test(client, f"USER {nickname}1 0 * :&{username}", f":{server_name} 432 * :Erroneous username")
    make_test(client, f"USER {nickname}1 0 * :+{username}", f":{server_name} 432 * :Erroneous username")
    make_test(client, f"USER {nickname}1 0 * :{username}1a", f":{server_name} 432 * :Erroneous username")
    
    # test too long username
    make_test(client, f"USER {nickname}1 0 * :tooooooooooooooolong", f":{server_name} 432 * :Erroneous username")

    # test invalid nickname
    make_test(client, f"USER {nickname}8 0 * :{username}", None)
    
    # test valid nickname
    make_test(client, f"USER {nickname}1 0 * :{username}A", f":{server_name} 001 {nickname}1 :Welcome to the IRC network")
    make_test(client2, f"USER {nickname}2 0 * :{username}B", f":{server_name} 001 {nickname}2 :Welcome to the IRC network")

    # test double execute USER
    make_test(client2, f"USER {nickname}2 0 * :{username}B", f":{server_name} 462 * :You may not reregister")