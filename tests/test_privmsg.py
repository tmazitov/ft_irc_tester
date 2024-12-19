from .test import make_test, make_dual_test

def gen_long_message():
    return "a" * 520

def test_privmsg(clients, server_name):
    
    print("\nPRIVMSG tests:\n")

    msg = gen_long_message()

    # test not enough or invalid params
    make_test(clients[0].socket, f"PRIVMSG",                              f":{server_name} 461 {clients[0].nickname} PRIVMSG :Not enough parameters")
    make_test(clients[0].socket, f"PRIVMSG {clients[0].nickname}",        f":{server_name} 461 {clients[0].nickname} PRIVMSG :Not enough parameters")
    make_test(clients[0].socket, f"PRIVMSG {clients[1].nickname} :",      f":{server_name} 412 {clients[0].nickname} PRIVMSG :No text to send")
    make_test(clients[0].socket, f"PRIVMSG {clients[1].nickname} : {msg}",f":{server_name} 417 {clients[0].nickname} PRIVMSG :Input line was too long")

    # test not found user or channel
    make_test(clients[0].socket, f"PRIVMSG notfound :hi!",     f":{server_name} 401 {clients[0].nickname} notfound :No such nick/channel")
    make_test(clients[0].socket, f"PRIVMSG #no_chanel :hi!",   f":{server_name} 403 {clients[0].nickname} #no_chanel :No such channel")

    # test to send to yourself
    make_test(clients[0].socket, f"PRIVMSG {clients[0].nickname} :hi!",   f":{server_name} 502 {clients[0].nickname} :Cannot send to yourself")

    # test send from client1 to client2
    make_dual_test(clients[0].socket, clients[1].socket, 
    f"PRIVMSG {clients[1].nickname} :hi!", 
    f":{clients[0].nickname}!{clients[0].username}@localhost PRIVMSG {clients[1].nickname} :hi!")

    # test send message from client2 to client1 with away status
    make_test(clients[0].socket, f"AWAY :I'm away", f":{server_name} 306 {clients[0].nickname} :You have been marked as being away")
    make_test(clients[1].socket, f"PRIVMSG {clients[0].nickname} :hello bro, how are you?", f":{server_name} 301 {clients[1].nickname} {clients[0].nickname} :I'm away")
    make_test(clients[0].socket, f"AWAY", f":{server_name} 305 {clients[0].nickname} :You are no longer marked as being away")

    #:<server_name> 305 <sender_nick> :You are no longer marked as being away

    #:<server_name> 404 <sender_nick> #private_channel :Cannot send to channel
    #:<server_name> 301 <sender_nick> JohnDoe :Away message text
    #:<server_name> 476 <sender_nick> @channel :Invalid channel name
