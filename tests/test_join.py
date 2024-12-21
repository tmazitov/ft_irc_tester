from .test import make_test, make_dual_test, make_broadcast_test

def test_join(clients, server_name):
    
    print("\nJOIN tests:\n")

    # test not enough or invalid params
    make_test(clients[0].socket, "JOIN", f":{server_name} 461 {clients[0].nickname} JOIN :Not enough parameters")
    make_test(clients[0].socket, "JOIN a", f":{server_name} 403 {clients[0].nickname} a :No such channel")
    make_test(clients[0].socket, "JOIN #", f":{server_name} 403 {clients[0].nickname} # :No such channel")

    channels = [
        "#without_password",
        "#with_password1",
        "#with_password2",
    ]

    # test right connection
    make_broadcast_test(clients[0].socket, [], f"JOIN {channels[0]}", [
        f":{clients[0].nickname}!{clients[0].username}@localhost JOIN :{channels[0]}",
        f":{server_name} 331 {clients[0].nickname} {channels[0]} :No topic is set",
        f":{server_name} 353 {clients[0].nickname} = {channels[0]} :@{clients[0].nickname}",
        f":{server_name} 366 {clients[0].nickname} {channels[0]} :End of /NAMES list"
    ], [])
    make_broadcast_test(clients[1].socket, 
    [
        clients[0].socket
    ], 
    f"JOIN {channels[0]}", 
    [      
        f":{clients[1].nickname}!{clients[1].username}@localhost JOIN :{channels[0]}",
        f":{server_name} 331 {clients[1].nickname} {channels[0]} :No topic is set",
        f":{server_name} 353 {clients[1].nickname} = {channels[0]} :@{clients[0].nickname} {clients[1].nickname}",
        f":{server_name} 366 {clients[1].nickname} {channels[0]} :End of /NAMES list"
    ],
    [
        f":{clients[1].nickname}!{clients[1].username}@localhost JOIN :{channels[0]}"
    ])
    make_broadcast_test(clients[2].socket, 
    [
        clients[0].socket,
        clients[1].socket,
    ], 
    f"JOIN {channels[0]}", 
    [      
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channels[0]}",
        f":{server_name} 331 {clients[2].nickname} {channels[0]} :No topic is set",
        f":{server_name} 353 {clients[2].nickname} = {channels[0]} :@{clients[0].nickname} {clients[1].nickname} {clients[2].nickname}",
        f":{server_name} 366 {clients[2].nickname} {channels[0]} :End of /NAMES list"
    ],
    [
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channels[0]}",
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channels[0]}"
    ])
    
    # test with and without password
    make_broadcast_test(clients[0].socket, 
    [], f"JOIN {channels[1]},{channels[2]} pass", 
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost JOIN :{channels[1]}",
        f":{server_name} 331 {clients[0].nickname} {channels[1]} :No topic is set",
        f":{server_name} 353 {clients[0].nickname} = {channels[1]} :@{clients[0].nickname}",
        f":{server_name} 366 {clients[0].nickname} {channels[1]} :End of /NAMES list",
        f":{clients[0].nickname}!{clients[0].username}@localhost JOIN :{channels[2]}",
        f":{server_name} 331 {clients[0].nickname} {channels[2]} :No topic is set",
        f":{server_name} 353 {clients[0].nickname} = {channels[2]} :@{clients[0].nickname}",
        f":{server_name} 366 {clients[0].nickname} {channels[2]} :End of /NAMES list",
    ], [])

    # test wrong password
    
    make_broadcast_test(clients[1].socket, 
    [
        clients[0].socket
    ], 
    f"JOIN {channels[1]},{channels[2]} wrong_pass", 
    [
        f":{server_name} 475 {clients[1].nickname} {channels[1]} :Cannot join channel (+k)",
        f":{clients[1].nickname}!{clients[1].username}@localhost JOIN :{channels[2]}",
        f":{server_name} 331 {clients[1].nickname} {channels[2]} :No topic is set",
        f":{server_name} 353 {clients[1].nickname} = {channels[2]} :@{clients[0].nickname} {clients[1].nickname}",
        f":{server_name} 366 {clients[1].nickname} {channels[2]} :End of /NAMES list"
    ], [
        f":{clients[1].nickname}!{clients[1].username}@localhost JOIN :{channels[2]}"
    ])

    # test join to the same channel
    make_broadcast_test(clients[1].socket, 
    [], f"JOIN {channels[2]} wrong_pass", 
    [
        f":{server_name} 443 {clients[1].nickname} {channels[2]} :You are already on that channel",
    ], [])

    # test send message to channel and user

    make_broadcast_test(clients[0].socket,
    [
        clients[1].socket,
        clients[2].socket,
    ], 
    f"PRIVMSG {channels[2]},{clients[2].nickname} :hello everyone!",
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost PRIVMSG {channels[2]} :hello everyone!",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost PRIVMSG {channels[2]} :hello everyone!",
        f":{clients[0].nickname}!{clients[0].username}@localhost PRIVMSG {clients[2].nickname} :hello everyone!",
    ])

    # test to write to channel without join
    make_test(clients[2].socket, 
    f"PRIVMSG {channels[2]} :hello everyone!", 
    f":{server_name} 442 {clients[2].nickname} {channels[2]} :You're not on that channel")

    # test change nick
    make_broadcast_test(clients[2].socket, 
    [
        clients[0].socket,
        clients[1].socket,
    ],
    f"NICK {clients[2].nickname}1",
    [
        f":{clients[2].nickname}!{clients[2].username}@localhost NICK :{clients[2].nickname}1",
    ],
    [
        f":{clients[2].nickname}!{clients[2].username}@localhost NICK :{clients[2].nickname}1",
        f":{clients[2].nickname}!{clients[2].username}@localhost NICK :{clients[2].nickname}1",
    ])

    clients[2].nickname = f"{clients[2].nickname}1"