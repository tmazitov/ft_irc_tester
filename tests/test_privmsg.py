from .test import make_test, make_dual_test

def gen_long_message():
    return "a" * 520

def test_privmsg(client, client2, username, nickname, nickname2, server_name):
    
    print("\nPRIVMSG tests:\n")

    msg = gen_long_message()

    # test not enough or invalid params
    make_test(client, f"PRIVMSG",                   f":{server_name} 461 {nickname} PRIVMSG :Not enough parameters")
    make_test(client, f"PRIVMSG {nickname}",        f":{server_name} 461 {nickname} PRIVMSG :Not enough parameters")
    make_test(client, f"PRIVMSG {nickname} :",      f":{server_name} 412 {nickname} PRIVMSG :No text to send")
    make_test(client, f"PRIVMSG {nickname} : {msg}",f":{server_name} 417 {nickname} PRIVMSG :Input line was too long")

    # test not found user or channel
    make_test(client, f"PRIVMSG notfound :hi!",     f":{server_name} 401 {nickname} notfound :No such nick/channel")
    make_test(client, f"PRIVMSG #no_chanel :hi!",   f":{server_name} 403 {nickname} #no_chanel :No such channel")

    # test to send to yourself
    make_test(client, f"PRIVMSG {nickname} :hi!",   f":{server_name} 502 {nickname} :Cannot send to yourself")

    # test send from client1 to client2
    make_dual_test(client, client2, f"PRIVMSG {nickname2} :hi!", f":{nickname}!{username}@localhost PRIVMSG {nickname2} :hi!")

    # test send message from client2 to client1 with away status
    make_test(client, f"AWAY :I'm away", f":{server_name} 306 {nickname} :You have been marked as being away")
    make_test(client2, f"PRIVMSG {nickname} :hello bro, how are you?", f":{server_name} 301 {nickname2} {nickname} :I'm away")
    make_test(client, f"AWAY", f":{server_name} 305 {nickname} :You are no longer marked as being away")

    #:<server_name> 305 <sender_nick> :You are no longer marked as being away

    #:<server_name> 404 <sender_nick> #private_channel :Cannot send to channel
    #:<server_name> 301 <sender_nick> JohnDoe :Away message text
    #:<server_name> 476 <sender_nick> @channel :Invalid channel name
