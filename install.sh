#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "Usage: install.sh <host> <port> <password> <server_name>"
    exit 1
fi

# Declare the variables
HOST="$1"
PORT="$2"
PASSWORD="$3"
SERVER_NAME="$4"

# Generate the script
cat << EOF > ./run_test_client.sh
#!/bin/bash

if [ "\$#" -ne 2 ]; then
    echo "Usage: run_test_client.sh <client_nickname> <client_username>"
    exit 1
fi

HOST="$HOST"
PORT=$PORT
PASSWORD="$PASSWORD"
CLIENT_NICKNAME="\$1"
CLIENT_USERNAME="\$2"

python3 test_client.py "\$HOST" "\$PORT" "\$PASSWORD" "\$CLIENT_NICKNAME" "\$CLIENT_USERNAME"
EOF

cat << EOF > ./run_test_auto.sh
#!/bin/bash

HOST="$HOST"
PORT=$PORT
PASSWORD="$PASSWORD"
SERVER_NAME="$SERVER_NAME"

python3 main.py "\$HOST" "\$PORT" "\$PASSWORD" "\$SERVER_NAME"
EOF



# Make the generated script executable
chmod +x ./run_test_client.sh
chmod +x ./run_test_auto.sh

echo "✅ Tester installed successfully!"
echo "* For hand testing use ./run_test_client.sh <client_nickname> <client_username>"
echo "* For auto testing use ./run_test_auto.sh | tee test_results.txt"
