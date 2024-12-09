import socket
import pprint

from state import unpack_state


PORT = 5000
SERVER = "hairo.local"
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()


try:
    while True:
        client, addr = server.accept()
        data = client.recv(1024)

        if data == b"":  # Disconnected
            client.close()
            continue

        system_state, footer_state, arm_state, collection_state = unpack_state(data)

        pprint.pprint(system_state)
        pprint.pprint(footer_state)
        pprint.pprint(arm_state)
        pprint.pprint(collection_state)

        client.sendall("ok".encode("utf-8"))
        client.close()

except KeyboardInterrupt as e:
    print("Finished!")
    server.close()

finally:
    server.close()
    print("Server closed!")
