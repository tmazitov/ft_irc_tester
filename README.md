# ft_irc_tester

Small tester for your irc server. You can choose 2 options:
* let the program test your IRC server
* test server by yourself with ready to use client

### How to install
```bash
./install.sh <host> <port> <password> <server_name>
```
This script will create 2 another scripts. One for the hand testing, another to make it automatically.

### How to run automatic test
Program will test your IRC server

1. Run your IRC server.

2. Open run_test_auto.sh and update variables HOST, PORT, PASSWORD and SERVER_NAME with your data. 

3. Run this command in the root folder of tester:
```bash
./run_test_auto.sh
```

### How to run test client
Program will create an authorized client connection

1. Run your IRC server.

2. Open run_test_client.sh and update variables HOST, PORT and PASSWORD with your data.

3. Run this command in the root folder of tester:
```bash
./run_test_client.sh <client_nickname> <client_username>
```
