from client.client import send_command

def make_test(client, request, expected_response):
    response = send_command(client, request, expected_response is None)
    if response is not None:
        response = response.replace("\r\n", "")
    # response.replace("\r", "")
    test_status = response == expected_response

    if test_status:
        print(f"✅ Test passed: {request}")
        if response:
            print(f"\t{response}")
        else:
            print("\t'No response'")
    else:
        print(f"❌ Test failed: {request}")
        print(f"\tExpected: {expected_response}")
        print(f"\tReceived: {response}")

def make_broadcast_test(sender, recipient_clients, command, expected_sender_response, expected_recipient_responses):
    
    # Sender send message
    sender.sendall(f"{command}\r\n".encode('utf-8'))
    
    # Sender wait for response
    
    try:
        response = sender.recv(4096).decode('utf-8')
    except TimeoutError:
        if expected_sender_response is None:
            response = None
        else:
            response = "TimeoutError"
    
    if response is not None:
        response = response.replace("\r\n", "")

    # Recipient wait for response

    recipient_responses = []
    for index, recipient in enumerate(recipient_clients):
        recipient.settimeout(10)
        try:
            recipient_response = recipient.recv(4096).decode('utf-8')
        except TimeoutError:
            if index < len(expected_recipient_responses) and expected_recipient_responses[index] is None:
                recipient_response = None
            else:
                recipient_response = "TimeoutError"
        
        if recipient_response is not None:
            recipient_response = recipient_response.replace("\r\n", "")
        
        recipient_responses.append(recipient_response)

    is_equal_sender_response = response == expected_sender_response
    is_equal_recipient_responses = all([recipient_responses[i] == expected_recipient_responses[i] for i in range(len(recipient_responses))])
    test_status = response == is_equal_sender_response and is_equal_recipient_responses

    if test_status:
        print(f"✅ Test passed: {command}")
        if response:
            print(f"\tSender: {response}")
        else:
            print("\tSender: 'No response'")
        if recipient_responses:
            print(f"\tRecipients: {recipient_responses[0]}")
        else:
            print(f"\tRecipients: 'No response'")

    else:
        print(f"❌ Test failed: {command}")
        print(f"\tExpected sender: {expected_sender_response}")
        print(f"\tReceived sender: {response}")
        for i, recipient_response in enumerate(recipient_responses):
            print(f"\tExpected recipient {i}: {expected_recipient_responses[i]}")
            print(f"\tReceived recipient {i}: {recipient_response}")


def make_dual_test(sender_client, recipient_client, command, expected_response):
    recipient_client.settimeout(10)
    sender_client.sendall(f"{command}\r\n".encode('utf-8'))
    try:
        response = recipient_client.recv(4096).decode('utf-8')
    except TimeoutError:
        if expected_response is None:
            response = None
        else:
            response = "TimeoutError"
    
    if response is not None:
        response = response.replace("\r\n", "")

    test_status = response == expected_response

    if test_status:
        print(f"✅ Test passed: {command}")
        if response:
            print(f"\t{response}")
        else:
            print("\t'No response'")
    else:
        print(f"❌ Test failed: {command}")
        print(f"\tExpected: {expected_response}")
        print(f"\tReceived: {response}")
