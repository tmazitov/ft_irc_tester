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
