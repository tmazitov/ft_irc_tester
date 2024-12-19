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