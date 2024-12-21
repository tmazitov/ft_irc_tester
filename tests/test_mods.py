from .test import make_test, make_broadcast_test
from client.client import send_command

# MODE #channel -k pass -- wrong

def test_mods(clients, server_name):
    print("\nMODE tests:\n")

    # MODE #channel +imk             ; Установить несколько режимов на канал
    # MODE #channel +k secretkey     ; Установить ключ для канала
    # MODE #channel -k               ; Убрать ключ с канала
    # MODE #nonexistent +m           ; Попытка установить режим для несуществующего канала
    # MODE #channel +k               ; Попытка установить ключ без указания ключа
    # MODE #channel +o user1         ; Назначить пользователя оператором
    # MODE #channel -o user1         ; Снять статус оператора с пользователя
    # MODE #channel +v user2         ; Дать пользователю право голоса
    # MODE #channel -v user2         ; Забрать право голоса у пользователя
    # MODE #channel +o               ; Попытка установить статус оператора без указания пользователя
    # MODE #channel +o user3         ; Попытка назначить оператором пользователя, не находящегося в канале
    # MODE #channel +z               ; Попытка установить неизвестный режим
    # MODE                           ; Отправка команды без аргументов
    # MODE !invalidchannel +m        ; Попытка установить режим для канала с некорректным именем
    # MODE #averylongchannelnamethatexceedslimits +m ; Попытка установить режим для канала с длинным именем

    channel = "#test_channel"
    print(send_command(clients[0].socket, f"JOIN {channel}"))
    print(send_command(clients[1].socket, f"JOIN {channel}"))
    clients[0].socket.settimeout(1)
    clients[1].socket.settimeout(1)
    for i in range(3):
        try:
            resp = clients[0].socket.recv(1024).decode("utf-8")
            print(resp)
        except:
            pass

        try:
            resp = clients[1].socket.recv(1024).decode("utf-8")
            print(resp)
        except:
            pass;
    
    # invalid channel tests

    make_test(clients[0].socket, 
    f"MODE", 
    f":{server_name} 461 {clients[0].nickname} MODE :Not enough parameters")
    
    make_test(clients[0].socket, 
    f"MODE {channel}",
    f":{server_name} 461 {clients[0].nickname} MODE :Not enough parameters")
    
    make_test(clients[0].socket, 
    f"MODE not_chan -i",
    f":{server_name} 403 {clients[0].nickname} not_chan :No such channel")
    
    make_test(clients[0].socket, 
    f"MODE #not_exists -i",
    f":{server_name} 403 {clients[0].nickname} #not_exists :No such channel")
    
    make_test(clients[0].socket, 
    f"MODE {channel} z", 
    f":{server_name} 472 {clients[0].nickname} z :is unknown mode char to me")
    
    make_broadcast_test(clients[0].socket, 
    [], 
    f"MODE {channel} -z -y -x",
    [
        f":{server_name} 472 {clients[0].nickname} z :is unknown mode char to me",
        f":{server_name} 472 {clients[0].nickname} y :is unknown mode char to me",
        f":{server_name} 472 {clients[0].nickname} x :is unknown mode char to me"
    ],[], )

    # +/-k tests

    make_broadcast_test(clients[0].socket, 
    [
        clients[1].socket
    ], 
    f"MODE {channel} +k pass", 
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +k",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +k",    
    ])

    make_test(clients[2].socket, f"JOIN {channel}", f":{server_name} 475 {clients[2].nickname} {channel} :Cannot join channel (+k)");
    make_test(clients[2].socket, f"JOIN {channel} pass1", f":{server_name} 475 {clients[2].nickname} {channel} :Cannot join channel (+k)");
    make_broadcast_test(clients[2].socket, 
    [
        clients[0].socket,
        clients[1].socket
    ],
    f"JOIN {channel} pass", 
    [
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channel}",
        f":{server_name} 331 {clients[2].nickname} {channel} :No topic is set",
        f":{server_name} 353 {clients[2].nickname} = {channel} :@{clients[0].nickname} {clients[1].nickname} {clients[2].nickname}",
        f":{server_name} 366 {clients[2].nickname} {channel} :End of /NAMES list"
    ],
    [
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channel}",
        f":{clients[2].nickname}!{clients[2].username}@localhost JOIN :{channel}",
    ])
    make_test(clients[2].socket, f"MODE {channel} -k", f":{server_name} 482 {clients[2].nickname} {channel} :You're not channel operator")
    make_broadcast_test(clients[0].socket, 
    [
        clients[1].socket,
        clients[2].socket,
    ], 
    f"MODE {channel} -k",
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} -k",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} -k",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} -k",
    ])

    
    # +/-o tests

    make_test(clients[0].socket, f"MODE {channel} +o", f":{server_name} 461 {clients[0].nickname} MODE :Not enough parameters")
    make_test(clients[0].socket, f"MODE {channel} +o nonmember", f":{server_name} 401 {clients[0].nickname} nonmember {channel} :No such nick/channel")
    make_test(clients[2].socket, f"MODE {channel} +o {clients[0].nickname}", f":{server_name} 482 {clients[2].nickname} {channel} :You're not channel operator")
    make_broadcast_test(clients[0].socket, 
    [
        clients[1].socket,
        clients[2].socket,
    ],
    f"MODE {channel} +o {clients[2].nickname}",
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[2].nickname}",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[2].nickname}",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[2].nickname}",
    ])
    make_test(clients[2].socket, f"MODE {channel} -o {clients[1].nickname}", f":{server_name} 482 {clients[2].nickname} {channel} :You're not channel operator")

    # +k +o test

    make_broadcast_test(clients[0].socket,
    [
        clients[1].socket,
        clients[2].socket,
    ],
    f"MODE {channel} +k pass +o {clients[1].nickname}",
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +k",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[1].nickname}",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +k",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[1].nickname}",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +k",
        f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} +o {clients[1].nickname}",
    ])

    # +/-l test

    result = send_command(clients[0].socket, f"JOIN {channel}1")
    while result != None:
        try:
            result = clients[0].socket.recv(1024).decode("utf-8")
        except:
            result = None

    make_test(clients[0].socket,
    f"MODE {channel}1 +l -1",
    f":{server_name} 696 {clients[0].nickname} {channel}1 +l :Invalid parameter",)

    make_test(clients[0].socket,
    f"MODE {channel}1 +l 101",
    f":{server_name} 696 {clients[0].nickname} {channel}1 +l :Invalid parameter",)

    make_test(clients[0].socket,
    f"MODE {channel}1 +l 1",
    f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel}1 +l 1")

    make_test(clients[1].socket,
    f"JOIN {channel}1",
    f":{server_name} 471 {clients[1].nickname} {channel}1 :Cannot join channel (+l)")
 
    make_test(clients[0].socket,
    f"MODE {channel}1 -l",
    f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel}1 -l")
    

    # +/-i tests

    make_test(clients[0].socket, 
    f"MODE {channel}1 +i", 
    f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel}1 +i")

    make_test(clients[1].socket,
    f"JOIN {channel}1",
    f":{server_name} 473 {clients[1].nickname} {channel}1 :Cannot join channel (+i)")

    make_broadcast_test(clients[0].socket,
    [
        clients[1].socket
    ],
    f"INVITE {clients[1].nickname} {channel}1",
    [
        f":{server_name} 341 {clients[0].nickname} {clients[1].nickname} {channel}1",
    ],
    [
        f":{clients[0].nickname}!{clients[0].username}@localhost INVITE {clients[1].nickname} :{channel}1",
    ])

    make_test(clients[0].socket, 
    f"MODE {channel}1 -i", 
    f":{clients[0].nickname}!{clients[0].username}@localhost MODE {channel} -i")
    
    make_test(clients[1].socket,
    f"JOIN {channel}1",
    f":{server_name} 473 {clients[1].nickname} {channel}1 :Cannot join channel (+i)")

    # +/- t tests

