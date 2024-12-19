if [ "$#" -ne 2 ]; then
    echo "Usage: run_test_client.sh <client_nickname> <client_username>"
    exit 1
fi

HOST="localhost"
PORT=6000
PASSWORD="password"
CLIENT_NICKNAME=$1
CLIENT_USERNAME=$2

python3 test_client.py $HOST $PORT $PASSWORD $CLIENT_NICKNAME $CLIENT_USERNAME