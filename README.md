# ft_irc_tester

Small tester for your irc server. 

## How to run automatic test (programm will test your IRC server)

1. Run your IRC server.

2. Open run_test_auto.sh and update variables HOST, PORT, PASSWORD and SERVER_NAME with your data. 

3. Run this command in the root folder of tester:
```bash
    ./run_test_auto.sh
```

## How to run hand test (programm will create an autorized client connection)

1. Run your IRC server.

2. Open run_test_auto.sh and update variables HOST, PORT and PASSWORD with your data.

3. Run this command in the root folder of tester:
```bash
    ./run_test_client.sh <client_nickname> <client_username>
```
